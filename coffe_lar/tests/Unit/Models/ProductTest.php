<?php

namespace Tests\Unit\Models;

use App\Models\Category;
use App\Models\Product;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ProductTest extends TestCase
{
  use RefreshDatabase;

  /** @test */
  public function it_has_a_category_relationship()
  {
    // Tạo một Category
    $category = Category::factory()->create();

    // Tạo một Product với category_id
    $product = Product::factory()->create(['category_id' => $category->id]);

    // Kiểm tra quan hệ category
    $this->assertInstanceOf(Category::class, $product->category);
    $this->assertEquals($category->id, $product->category->id);
  }

  /** @test */
  public function it_handles_slug_accessor_and_mutator()
  {
    // Tạo product với name và slug giống nhau
    $product = Product::factory()->create([
      'name' => 'Test Product',
      'slug' => 'Test Product'  // Mutator sẽ tự động chuyển thành 'test-product'
    ]);

    // Kiểm tra rằng mutator đã chuyển đổi slug đúng
    $this->assertEquals('test-product', $product->slug);

    // Kiểm tra accessor
    $this->assertEquals('test-product', $product->slug);
  }

  /** @test */
  public function it_handles_thumb_image_accessor_and_mutator()
  {
    $product = Product::factory()->create(['thumb_image' => 'image.jpg']);

    // Accessor
    $this->assertEquals('image.jpg', $product->thumb_image);

    // Mutator
    $product->thumb_image = 'new_image.jpg';
    $this->assertEquals('new_image.jpg', $product->thumb_image);
  }

  /** @test */
  public function it_handles_mass_assignment()
  {
    $category = Category::factory()->create(); // Tạo Category trước

    // Tạo Product bằng mass assignment
    $product = Product::create([
      'thumb_image' => 'image.jpg',
      'name' => 'Test Product',
      'slug' => 'test-product',
      'category_id' => $category->id, // Gán category_id hợp lệ
      'description' => 'Test description',
      'content' => 'Test content',
      'price' => 1000,
      'status' => 1,
      'weight' => 500,
    ]);

    // Kiểm tra các thuộc tính đã được gán đúng
    $this->assertEquals('image.jpg', $product->thumb_image);
    $this->assertEquals('Test Product', $product->name);
    $this->assertEquals('test-product', $product->slug);
    $this->assertEquals($category->id, $product->category_id);
    $this->assertEquals('Test description', $product->description);
    $this->assertEquals('Test content', $product->content);
    $this->assertEquals(1000, $product->price);
    $this->assertEquals(1, $product->status);
    $this->assertEquals(500, $product->weight);
  }
}
