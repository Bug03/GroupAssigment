<?php

namespace Tests\Unit\Services;

use App\Http\Services\CartService;
use App\Models\Cart;
use App\Models\Product;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\ValidationException;
use Tests\TestCase;

class CartServiceTest extends TestCase
{
  use RefreshDatabase;

  protected $user;
  protected $cart;
  protected $product;

  public function setUp(): void
  {
    parent::setUp();

    // Tạo user test
    $this->user = User::factory()->create();

    // Tạo cart cho user
    $this->cart = Cart::factory()->create([
      'user_id' => $this->user->id,
      'cart_items' => json_encode([])
    ]);

    // Tạo sản phẩm test
    $this->product = Product::factory()->create();
  }

  /** @test */
  public function it_can_clear_cart()
  {
    // Login user
    Auth::login($this->user);

    // Thêm item vào cart
    $this->cart->saveCart($this->product->id, 2);

    // Gọi phương thức clear
    CartService::clear();

    // Kiểm tra cart đã trống
    $this->assertEmpty($this->cart->fresh()->getCartItems());
  }

  /** @test */
  public function it_can_get_list_cart()
  {
    // Login user
    Auth::login($this->user);

    // Tạo nhiều sản phẩm ngẫu nhiên
    $products = [];
    $expectedSubtotal = 0;
    $expectedWeight = 0;

    for ($i = 0; $i < rand(3, 5); $i++) {
      $products[] = Product::factory()->create([
        'price' => rand(100000, 1000000),
        'weight' => rand(100, 1000)
      ]);
    }

    // Thêm sản phẩm vào cart với số lượng ngẫu nhiên
    foreach ($products as $product) {
      $quantity = rand(1, 5);
      $this->cart->saveCart($product->id, $quantity);

      // Tính toán tổng giá trị và cân nặng dự kiến
      $expectedSubtotal += $product->price * $quantity;
      $expectedWeight += $product->weight;
    }

    // Lấy danh sách cart
    $result = CartService::getListCart();

    // Kiểm tra cấu trúc kết quả
    $this->assertArrayHasKey('cartList', $result);
    $this->assertArrayHasKey('productList', $result);
    $this->assertArrayHasKey('weight', $result);
    $this->assertArrayHasKey('subtotal', $result);

    // Kiểm tra số lượng sản phẩm
    $this->assertCount(count($products), $result['productList']);

    // Kiểm tra tổng giá trị
    $this->assertEquals($expectedSubtotal, $result['subtotal']);

    // Kiểm tra tổng cân nặng
    $this->assertEquals($expectedWeight, $result['weight']);

    // Kiểm tra thông tin chi tiết từng sản phẩm
    foreach ($products as $product) {
        $cartItem = $result['cartList'][$product->id];

        // Kiểm tra thông tin sản phẩm trong cart
        $this->assertEquals($product->id, $cartItem['id_product']);
        $this->assertGreaterThan(0, $cartItem['quantity']);

        // Kiểm tra sản phẩm trong productList
        $productInList = $result['productList']->firstWhere('id', $product->id);
        $this->assertNotNull($productInList);
        $this->assertEquals($product->price, $productInList->price);
        $this->assertEquals($product->weight, $productInList->weight);

        // Kiểm tra tính toán giá tiền cho từng sản phẩm
        $expectedItemTotal = $product->price * $cartItem['quantity'];
        $actualItemTotal = $productInList->price * $cartItem['quantity'];
        $this->assertEquals($expectedItemTotal, $actualItemTotal);
    }
  }

  /** @test */
  public function it_returns_empty_array_for_guest_user()
  {
    // Không login user
    $result = CartService::getListCart();

    // Kiểm tra kết quả rỗng
    $this->assertEmpty($result);
  }

  /** @test */
  public function it_can_show_cart_item()
  {
    // Login user
    Auth::login($this->user);

    // Thêm sản phẩm vào cart
    $this->cart->saveCart($this->product->id, 2);

    // Khởi tạo CartService
    $cartService = new CartService();

    // Lấy thông tin item
    $result = $cartService->show($this->product->id);

    // Kiểm tra kết quả
    $this->assertEquals($this->product->id, $result->id);
    $this->assertEquals(2, $result->quantity);
  }

  /** @test */
  public function it_can_destroy_cart_item()
  {
    // Login user
    Auth::login($this->user);

    // Thêm sản phẩm vào cart
    $this->cart->saveCart($this->product->id, 2);

    // Khởi tạo CartService
    $cartService = new CartService();

    // Xóa item
    $cartService->destroy($this->product->id);

    // Kiểm tra item đã bị xóa
    $this->assertArrayNotHasKey($this->product->id, $this->cart->fresh()->getCartItems());
  }

  /** @test */
  public function it_can_store_new_cart_item()
  {
    // Login user
    Auth::login($this->user);

    // Khởi tạo CartService
    $cartService = new CartService();

    // Thêm sản phẩm mới
    $cartService->store($this->product->id, 2);

    // Kiểm tra sản phẩm đã được thêm
    $cartItems = $this->cart->fresh()->getCartItems();
    $this->assertArrayHasKey($this->product->id, $cartItems);
    $this->assertEquals(2, $cartItems[$this->product->id]['quantity']);
  }

  /** @test */
  public function it_throws_exception_for_invalid_quantity()
  {
    // Login user
    Auth::login($this->user);

    // Khởi tạo CartService
    $cartService = new CartService();

    // Kiểm tra ném exception khi số lượng không hợp lệ
    $this->expectException(ValidationException::class);
    $cartService->store($this->product->id, 0);
  }

  /** @test */
  public function it_can_count_cart_items()
  {
    // Login user
    Auth::login($this->user);

    // Thêm sản phẩm vào cart
    $this->cart->saveCart($this->product->id, 2);

    // Đếm số lượng item
    $count = CartService::countCart();

    // Kiểm tra kết quả
    $this->assertEquals(1, $count);
  }
}
