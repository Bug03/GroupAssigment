<?php

namespace Tests\Unit\Models;

use App\Models\Order;
use App\Models\User;
use App\Models\OrderProduct;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class OrderTest extends TestCase #4
{
  use RefreshDatabase;

  /** @test */
  public function it_belongs_to_a_user()
  {
    $user = User::factory()->create();
    $order = Order::factory()->create(['user_id' => $user->id]);

    $this->assertInstanceOf(User::class, $order->user);
    $this->assertEquals($user->id, $order->user->id);
  }

  /** @test */
  public function it_has_many_order_products()
  {
    $order = Order::factory()->create();
    $orderProduct1 = OrderProduct::factory()->create(['order_id' => $order->id]);
    $orderProduct2 = OrderProduct::factory()->create(['order_id' => $order->id]);

    $this->assertCount(2, $order->orderProducts);
    $this->assertTrue($order->orderProducts->contains($orderProduct1));
    $this->assertTrue($order->orderProducts->contains($orderProduct2));
  }

  /** @test */
  public function it_handles_name_receiver_mutator_and_accessor()
  {
    $order = Order::factory()->create(['name_receiver' => 'John Doe']);

    $this->assertEquals('John Doe', $order->name_receiver);

    $order->name_receiver = 'Jane Doe';
    $this->assertEquals('Jane Doe', $order->name_receiver);
  }

  /** @test */
  public function it_handles_sub_total_mutator_and_accessor()
  {
    $order = Order::factory()->create(['sub_total' => 100.00]);

    $this->assertEquals(100.00, $order->sub_total);

    $order->sub_total = 200.00;
    $this->assertEquals(200.00, $order->sub_total);
  }
}
