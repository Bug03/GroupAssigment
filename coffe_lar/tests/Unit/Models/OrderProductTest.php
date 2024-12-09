<?php

namespace Tests\Unit\Models;

use App\Models\Order;
use App\Models\OrderProduct;
use App\Models\Product;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class OrderProductTest extends TestCase
{
  use RefreshDatabase;

  /** @test */
  public function it_belongs_to_an_order()
  {
    $order = Order::factory()->create();
    $orderProduct = OrderProduct::factory()->create(['order_id' => $order->id]);

    $this->assertEquals($order->id, $orderProduct->order_id);
  }

  /** @test */
  public function it_has_product_details()
  {
    $orderProduct = OrderProduct::factory()->create([
      'product_name' => 'Sample Product',
      'product_price' => 100.50,
      'qty' => 2,
    ]);

    $this->assertEquals('Sample Product', $orderProduct->product_name);
    $this->assertEquals(100.50, $orderProduct->product_price);
    $this->assertEquals(2, $orderProduct->qty);
  }

  /** @test */
  public function it_handles_order_id_accessor_and_mutator()
  {
    $order = \App\Models\Order::factory()->create();
    $newOrder = \App\Models\Order::factory()->create(); // Tạo một Order mới để kiểm tra mutator
    $orderProduct = \App\Models\OrderProduct::factory()->create(['order_id' => $order->id]);

    // Kiểm tra Accessor
    $this->assertEquals($order->id, $orderProduct->order_id);

    // Kiểm tra Mutator
    $orderProduct->order_id = $newOrder->id; // Sử dụng order_id hợp lệ
    $orderProduct->save();

    $this->assertEquals($newOrder->id, $orderProduct->order_id);
  }

  /** @test */
  public function it_handles_product_id_accessor_and_mutator()
  {
    $product = \App\Models\Product::factory()->create();
    $newProduct = \App\Models\Product::factory()->create(); // Tạo một Product mới để kiểm tra mutator
    $orderProduct = \App\Models\OrderProduct::factory()->create(['product_id' => $product->id]);

    // Kiểm tra Accessor
    $this->assertEquals($product->id, $orderProduct->product_id);

    // Kiểm tra Mutator
    $orderProduct->product_id = $newProduct->id; // Sử dụng product_id hợp lệ
    $orderProduct->save();

    $this->assertEquals($newProduct->id, $orderProduct->product_id);
  }
}
