<?php

namespace Tests\Unit\Requests;

use App\Http\Requests\Backend\CategoryRequest;
use App\Models\Category;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Validator;
use Tests\TestCase;

class CategoryRequestTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        $this->request = new CategoryRequest();
    }

    /** @test */
    public function it_requires_icon()
    {
        $validator = Validator::make(
            ['icon' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('icon', $validator->errors()->messages());
    }

    /** @test */
    public function icon_must_be_string()
    {
        $validator = Validator::make(
            ['icon' => 123],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('icon', $validator->errors()->messages());
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
        $existingCategory = Category::factory()->create([
            'name' => 'Test Category',
            'slug' => 'test-category'
        ]);

        // Test case 1: Kiểm tra tên trùng chính xác
        $validator = Validator::make(
            ['name' => 'Test Category'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());

        // Test case 2: Kiểm tra tên khác nhưng tạo ra slug trùng
        $validator = Validator::make(
            ['name' => 'Test  Category'], // 2 khoảng trắng
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
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
        $validator = Validator::make([
            'icon' => 'fa-category',
            'name' => 'Valid Category Name',
            'status' => 1
        ], $this->request->rules());

        $this->assertFalse($validator->fails());
    }
} 
