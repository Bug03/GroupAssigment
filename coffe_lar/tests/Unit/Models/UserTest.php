<?php

namespace Tests\Unit\Models;

use App\Models\Cart;
use App\Models\Role;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserTest extends TestCase
{
  use RefreshDatabase;

  /** @test */
  public function it_has_a_role_relationship() # Kiểm tra quan hệ belongsTo giữa User và Role.
  {
    // Tạo một Role
    $role = Role::factory()->create();

    // Tạo một User và gắn role_id
    $user = User::factory()->create(['role_id' => $role->id]);

    // Kiểm tra quan hệ role
    $this->assertInstanceOf(Role::class, $user->role);
    $this->assertEquals($role->id, $user->role->id);
  }

  /** @test */
  public function it_has_a_cart_relationship() # Kiểm tra quan hệ hasOne giữa User và Cart.
  {
    $role = Role::factory()->create(); // Tạo Role trước

    $user = User::factory()->create(['role_id' => $role->id]); // Gắn role_id hợp lệ
    $cart = Cart::factory()->create(['user_id' => $user->id]);

    $this->assertInstanceOf(Cart::class, $user->cart);
    $this->assertEquals($cart->id, $user->cart->id);
  }

  /** @test */
  public function it_handles_name_accessor_and_mutator() # Kiểm tra Accessor và Mutator của thuộc tính name.
  {
    $role = Role::factory()->create(); // Tạo Role trước

    $user = User::factory()->create(['name' => 'John Doe', 'role_id' => $role->id]);

    // Kiểm tra Accessor
    $this->assertEquals('John Doe', $user->name);

    // Kiểm tra Mutator
    $user->name = 'Jane Doe';
    $this->assertEquals('Jane Doe', $user->name);
  }

  /** @test */
  public function it_handles_email_accessor_and_mutator() #Kiểm tra Accessor và Mutator của thuộc tính email.
  {
    $role = Role::factory()->create(); // Tạo Role trước

    $user = User::factory()->create(['email' => 'test@example.com', 'role_id' => $role->id]);

    // Kiểm tra Accessor
    $this->assertEquals('test@example.com', $user->email);

    // Kiểm tra Mutator
    $user->email = 'new@example.com';
    $this->assertEquals('new@example.com', $user->email);
  }
  /** @test */
  public function it_has_fillable_attributes() # Kiểm tra khả năng gán hàng loạt (mass assignment) các thuộc tính trong $fillable của User.
  {
    $role = Role::factory()->create(); // Tạo Role trước

    // Tạo một User bằng mass assignment
    $user = User::create([
      'name' => 'John Doe',
      'email' => 'test@example.com',
      'password' => bcrypt('password'),
      'phone' => '123456789',
      'role_id' => $role->id, // Sử dụng role_id hợp lệ
      'status' => 1, // Gán số nguyên thay vì chuỗi nếu cột status yêu cầu
    ]);

    // Kiểm tra các thuộc tính đã được gán đúng
    $this->assertEquals('John Doe', $user->name);
    $this->assertEquals('test@example.com', $user->email);
    $this->assertEquals('123456789', $user->phone);
    $this->assertEquals($role->id, $user->role_id);
    $this->assertEquals(1, $user->status);
  }
}
