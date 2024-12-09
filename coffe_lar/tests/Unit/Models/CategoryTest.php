<?php

namespace Tests\Unit\Models;

use App\Models\Category;
use App\Models\Product;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Str;
use Tests\TestCase;

class CategoryTest extends TestCase #6
{
  use RefreshDatabase;

  /** @test */
  public function it_has_a_products_relationship()
  {
    // Tạo một Category
    $category = Category::factory()->create();

    // Tạo các Product liên kết với Category
    $product1 = Product::factory()->create([
      'category_id' => $category->id,
      'name' => 'Product One',
      'slug' => 'product-one'  // Thêm slug duy nhất
    ]);

    $product2 = Product::factory()->create([
      'category_id' => $category->id,
      'name' => 'Product Two',
      'slug' => 'product-two'  // Thêm slug duy nhất
    ]);

    // Kiểm tra quan hệ products
    $this->assertCount(2, $category->products);
    $this->assertTrue($category->products->contains($product1));
    $this->assertTrue($category->products->contains($product2));
  }

  /** @test */
  public function it_handles_slug_accessor_and_mutator()
  {
    // Tạo Category với name và slug
    $category = Category::factory()->create([
      'name' => 'Test Category',
      'slug' => 'test-category'  // thêm slug trực tiếp
    ]);

    // Kiểm tra accessor và mutator
    $this->assertEquals('test-category', $category->slug);
    $this->assertEquals('test-category', $category->slug);
  }

  /** @test */
  public function it_handles_name_accessor_and_mutator()
  {
    $category = Category::factory()->create(['name' => 'Sample Name']);

    // Kiểm tra Accessor
    $this->assertEquals('Sample Name', $category->name);

    // Kiểm tra Mutator
    $category->name = 'Updated Name';
    $this->assertEquals('Updated Name', $category->name);
  }

  /** @test */
  public function it_handles_icon_accessor_and_mutator()
  {
    $category = Category::factory()->create(['icon' => 'icon.png']);

    // Kiểm tra Accessor
    $this->assertEquals('icon.png', $category->icon);

    // Kiểm tra Mutator
    $category->icon = 'new-icon.png';
    $this->assertEquals('new-icon.png', $category->icon);
  }

  /** @test */
  public function it_handles_status_accessor_and_mutator()
  {
    $category = Category::factory()->create(['status' => 1]);

    // Kiểm tra Accessor
    $this->assertEquals(1, $category->status);

    // Kiểm tra Mutator
    $category->status = 0;
    $this->assertEquals(0, $category->status);
  }

  /** @test */
  public function it_handles_mass_assignment()
  {
    // Tạo Category bằng mass assignment
    $category = Category::create([
      'name' => 'Mass Assigned Category',
      'icon' => 'icon.jpg',
      'status' => 1,
      'slug' => Str::slug('Mass Assigned Category'),
    ]);

    // Kiểm tra các thuộc tính
    $this->assertEquals('Mass Assigned Category', $category->name);
    $this->assertEquals('icon.jpg', $category->icon);
    $this->assertEquals(1, $category->status);
    $this->assertEquals('mass-assigned-category', $category->slug);
  }
}
