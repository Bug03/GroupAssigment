<?php
namespace Database\Factories;
use App\Enums\OrderStatus;
use App\Enums\PaymentStatus;
use App\Models\Order;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
class OrderFactory extends Factory
{
  protected $model = Order::class;
  public function definition()
  {
    return [
      'user_id' => User::factory(), // Liên kết với User
      'name_receiver' => $this->faker->name,
      'address_receiver' => $this->faker->address,
      'phone_receiver' => $this->faker->phoneNumber,
      'email_receiver' => $this->faker->safeEmail,
      'note' => $this->faker->sentence,
      'sub_total' => $this->faker->randomFloat(2, 50, 1000), // Tổng phụ
      'fee_ship' => $this->faker->randomFloat(2, 5, 50),    // Phí vận chuyển
      'total' => $this->faker->randomFloat(2, 100, 1500),   // Tổng cộng
      'payment_status' => $this->faker->randomElement([     // Trạng thái thanh toán
        PaymentStatus::OptionOne,
        PaymentStatus::OptionTwo,
        PaymentStatus::OptionThree,
      ]),
      'order_status' => $this->faker->randomElement([       // Trạng thái đơn hàng
        OrderStatus::pending,
        OrderStatus::processed_and_ready_to_ship,
        OrderStatus::out_for_delivery,
        OrderStatus::delivered,
        OrderStatus::canceled,
      ]),
    ];
  }
}
