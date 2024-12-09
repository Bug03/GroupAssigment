<?php

namespace Database\Factories;

use App\Models\Order;
use App\Models\OrderProduct;
use App\Models\Product;
use Illuminate\Database\Eloquent\Factories\Factory;

class OrderProductFactory extends Factory
{
  protected $model = OrderProduct::class;

  public function definition()
  {
    return [
      'order_id' => Order::factory(), // Tạo liên kết với một Order
      'product_id' => Product::factory(), // Tạo liên kết với một Product
      'product_name' => $this->faker->word, // Tên sản phẩm giả lập
      'product_price' => $this->faker->randomFloat(2, 10, 1000), // Giá sản phẩm
      'qty' => $this->faker->numberBetween(1, 10), // Số lượng sản phẩm
    ];
  }
}
