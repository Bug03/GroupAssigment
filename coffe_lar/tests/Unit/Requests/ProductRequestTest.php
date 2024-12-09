<?php

namespace Tests\Unit\Requests;

use App\Http\Requests\Backend\ProductRequest;
use App\Models\Category;
use App\Models\Product;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Validator;
use Tests\TestCase;

class ProductRequestTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        $this->request = new ProductRequest();
    }

    /** @test */
    public function it_requires_name()
    {
        $validator = Validator::make(
            ['name' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('name', $validator->errors()->messages());
    }

    /** @test */
    public function name_must_not_exceed_200_characters()
    {
        $validator = Validator::make(
            ['name' => str_repeat('a', 201)],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('name', $validator->errors()->messages());
    }

    /** @test */
    public function name_must_be_unique_by_slug()
    {
        // Arrange
        $existingProduct = Product::factory()->create([
            'name' => 'Test Product',
            'slug' => 'test-product'
        ]);

        // Test case 1: Kiểm tra tên trùng chính xác
        $validator = Validator::make(
            ['name' => 'Test Product'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());

        // Test case 2: Kiểm tra tên khác nhưng tạo ra slug trùng
        $validator = Validator::make(
        ['name' => 'Test  Product'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
    }

    /** @test */
    public function it_requires_category_id()
    {
        $validator = Validator::make(
            ['category_id' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('category_id', $validator->errors()->messages());
    }

    /** @test */
    public function category_id_must_exist_in_categories_table()
    {
        // Test case 1: Gửi category_id không tồn tại
        $validator = Validator::make(
            ['category_id' => 999], // Giả lập form submit với category_id không tồn tại
            $this->request->rules()
        );

        // Validation phải fail vì category_id không tồn tại trong DB
        $this->assertTrue($validator->fails());

        // Test case 2: Gửi category_id hợp lệ
        $category = Category::factory()->create([
            'status' => true
        ]);

        $validator = Validator::make(
            ['category_id' => $category->id], // Giả lập form submit với category_id hợp lệ
            $this->request->rules()
        );


        $this->assertDatabaseHas('categories', [
            'id' => $category->id,
            'status' => true
        ]);
    }

    /** @test */
    public function thumb_image_must_be_valid_image()
    {
        $validator = Validator::make(
            ['thumb_image' => 'not-an-image'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('thumb_image', $validator->errors()->messages());
    }

    /** @test */
    public function thumb_image_must_not_exceed_3mb()
    {
        $validator = Validator::make(
            ['thumb_image' => 'large-image'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('thumb_image', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_price()
    {
        $validator = Validator::make(
            ['price' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('price', $validator->errors()->messages());
    }

    /** @test */
    public function price_must_be_integer()
    {
        $validator = Validator::make(
            ['price' => 'not-a-number'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('price', $validator->errors()->messages());
    }

    /** @test */
    public function price_must_be_at_least_1()
    {
        $validator = Validator::make(
            ['price' => 0],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('price', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_weight()
    {
        $validator = Validator::make(
            ['weight' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('weight', $validator->errors()->messages());
    }

    /** @test */
    public function weight_must_be_integer()
    {
        $validator = Validator::make(
            ['weight' => 'not-a-number'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('weight', $validator->errors()->messages());
    }

    /** @test */
    public function weight_must_be_at_least_1()
    {
        $validator = Validator::make(
            ['weight' => 0],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('weight', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_description()
    {
        $validator = Validator::make(
            ['description' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('description', $validator->errors()->messages());
    }

    /** @test */
    public function description_must_not_exceed_600_characters()
    {
        $validator = Validator::make(
            ['description' => str_repeat('a', 601)],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('description', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_content()
    {
        $validator = Validator::make(
            ['content' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('content', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_status()
    {
        $validator = Validator::make(
            ['status' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('status', $validator->errors()->messages());
    }

    /** @test */
    public function it_passes_with_valid_data()
    {
        $category = Category::factory()->create();

        $validator = Validator::make([
            'name' => 'Valid Product Name',
            'category_id' => $category->id,
            'price' => 100000,
            'weight' => 500,
            'description' => 'Valid description',
            'content' => 'Valid content',
            'status' => 1
        ], $this->request->rules());

        $this->assertFalse($validator->fails());
    }
}
