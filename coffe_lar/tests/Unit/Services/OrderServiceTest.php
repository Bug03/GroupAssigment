<?php

namespace Tests\Unit\Services;

use App\Http\Services\CartService;
use App\Http\Services\GiaoHangNhanhService;
use App\Http\Services\OrderService;
use App\Models\Order;
use App\Models\Product;
use App\Models\Role;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Cache;
use Tests\TestCase;
use Mockery;

class OrderServiceTest extends TestCase
{
    use RefreshDatabase;

    protected $orderService;
    protected $giaoHangNhanhService;
    protected $cartService;

    protected function setUp(): void
    {
        parent::setUp();
        $this->giaoHangNhanhService = $this->mock(GiaoHangNhanhService::class);
        $this->cartService = Mockery::mock('alias:' . CartService::class);
        $this->orderService = new OrderService($this->giaoHangNhanhService);
    }

    /**
     * Data provider for order test cases
     */
    public static function orderDataProvider(): array
    {
        return [
            'Successful Order Creation' => [
                'cart' => [
                    'cartList' => [
                        [
                            'quantity' => 2,
                            'price' => 100000,
                        ]
                    ],
                    'weight' => 1000,
                    'subtotal' => 200000
                ],
                'shipping_fee' => 30000,
                'should_succeed' => true,
                'expected_total' => 230000
            ],
            'Empty Cart Order' => [
                'cart' => [
                    'cartList' => [],
                    'weight' => 0,
                    'subtotal' => 0
                ],
                'shipping_fee' => 30000,
                'should_succeed' => false,
                'expected_exception' => \Symfony\Component\HttpKernel\Exception\HttpException::class
            ],
            'Shipping Calculation Error' => [
                'cart' => [
                    'cartList' => [
                        [
                            'quantity' => 1,
                            'price' => 100000,
                        ]
                    ],
                    'weight' => 1000,
                    'subtotal' => 100000
                ],
                'shipping_fee' => -1,
                'should_succeed' => false,
                'expected_exception' => \Symfony\Component\HttpKernel\Exception\HttpException::class
            ]
        ];
    }

    /**
    * @test
    * @dataProvider orderDataProvider
    */
    public function it_handles_order_creation(
        array $cart,
        int $shipping_fee,
        bool $should_succeed,
        $expected = null
    ) {
        echo "\n\n=== Starting Test Case ===\n";
        echo "Cart Data: " . json_encode($cart, JSON_PRETTY_PRINT) . "\n";
        echo "Shipping Fee: " . $shipping_fee . "\n";
        echo "Should Succeed: " . ($should_succeed ? 'Yes' : 'No') . "\n";
        echo "Expected Result: " . json_encode($expected) . "\n";

        // 1. Setup base test data
        echo "\n--- Setting up test data ---\n";
        $role = Role::factory()->create(['id' => 2]);
        $user = User::factory()->create([
            'role_id' => $role->id,
            'email' => 'test@example.com'
        ]);
        Auth::login($user);
        echo "Created User: " . $user->email . "\n";

        $category = \App\Models\Category::factory()->create([
            'name' => 'Test Category',
            'status' => true
        ]);
        $product = Product::factory()->create([
            'category_id' => $category->id,
            'name' => 'Test Product',
            'price' => 100000,
            'weight' => 500,
            'status' => true,
            'thumb_image' => 'test.jpg'
        ]);
        echo "Created Product: " . $product->name . " (Price: " . number_format($product->price) . " VND)\n";

        // 2. Setup request
        echo "\n--- Setting up request ---\n";
        $request = new Request();
        $request->merge([
            'province' => '1',
            'district' => '1',
            'ward' => '1',
            'name' => 'Test User',
            'phone' => '1234567890',
            'email' => 'test@example.com',
            'address' => '123 Test St',
            'note' => 'Test note'
        ]);
        echo "Request Data: " . json_encode($request->all(), JSON_PRETTY_PRINT) . "\n";

        // 3. Mock Cache
        echo "\n--- Mocking Cache ---\n";
        $this->mockCacheResponses();
        echo "Cache mocked for province, district, and ward\n";

        // 4. Mock Cart Service
        echo "\n--- Mocking Cart Service ---\n";
        if (!empty($cart['cartList'])) {
            $cart['cartList'][0]['product-data'] = $product;
            echo "Added product to cart: " . $product->name . "\n";
        }
        $this->cartService->shouldReceive('getListCart')->once()->andReturn($cart);
        echo "Cart service mocked with " . count($cart['cartList']) . " items\n";

        if ($should_succeed) {
            $this->cartService->shouldReceive('clear')->once()->andReturn(true);
            echo "Cart clear method mocked\n";
        }

        // 5. Mock Shipping Service
        echo "\n--- Mocking Shipping Service ---\n";
        $this->giaoHangNhanhService->shouldReceive('calculatePrice')
            ->once()
            ->andReturn($shipping_fee);
        echo "Shipping fee mocked: " . number_format($shipping_fee) . " VND\n";

        // 6. Execute and Assert
        echo "\n--- Executing Test ---\n";
        try {
            if (!$should_succeed) {
                $this->expectException($expected);
                echo "Expecting exception: " . $expected . "\n";
            }

            $response = $this->orderService->checkOutFormSubmit($request);
            echo "Order submission completed\n";

            if ($should_succeed) {
                echo "\n--- Verifying Database ---\n";
                // Verify order creation
                $order = Order::first();
                echo "Order created with ID: " . $order->id . "\n";
                echo "Total amount: " . number_format($order->total) . " VND\n";

                $this->assertDatabaseHas('orders', [
                    'user_id' => $user->id,
                    'name_receiver' => 'Test User',
                    'phone_receiver' => '1234567890',
                    'email_receiver' => 'test@example.com',
                    'sub_total' => $cart['subtotal'],
                    'fee_ship' => $shipping_fee,
                    'total' => $expected
                ]);
                echo "Order details verified in database\n";

                // Verify order products
                if (!empty($cart['cartList'])) {
                    $this->assertDatabaseHas('order_products', [
                        'order_id' => $order->id,
                        'product_id' => $product->id,
                        'product_name' => 'Test Product',
                        'product_price' => 100000,
                        'qty' => $cart['cartList'][0]['quantity']
                    ]);
                    echo "Order products verified in database\n";
                }
            }
        } catch (\Exception $e) {
            echo "\n--- Exception Caught ---\n";
            echo "Exception: " . get_class($e) . "\n";
            echo "Message: " . $e->getMessage() . "\n";
            throw $e;
        }

        echo "\n=== Test Case Completed ===\n";
    }

    private function mockCacheResponses(): void
    {
        Cache::shouldReceive('get')
            ->with('province')
            ->andReturn([
                'data' => [
                    ['ProvinceID' => '1', 'ProvinceName' => 'Test Province']
                ]
            ]);

        Cache::shouldReceive('get')
            ->with('district-1')
            ->andReturn([
                'data' => [
                    ['DistrictID' => '1', 'DistrictName' => 'Test District']
                ]
            ]);

        Cache::shouldReceive('get')
            ->with('ward-1')
            ->andReturn([
                'data' => [
                    ['WardCode' => '1', 'WardName' => 'Test Ward']
                ]
            ]);
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }
}
