<?php
namespace Database\Factories;
use App\Models\Cart;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
class CartFactory extends Factory
{
  protected $model = Cart::class;
  public function definition()
  {
    return [
      'user_id' => User::factory(), // Tạo một User liên quan
      'cart_items' => json_encode([
        [
          'id_product' => $this->faker->randomNumber(),
          'quantity' => $this->faker->numberBetween(1, 10),
        ],
      ]), // Giả lập dữ liệu sản phẩm trong giỏ
    ];
  }
}
