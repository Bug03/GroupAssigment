<?php
namespace Tests\Unit\Models;
use App\Models\Cart;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
class CartTest extends TestCase # 4
{
  use RefreshDatabase;
  /** @test */
  public function it_clears_cart_items()
  {
    $cart = Cart::factory()->create(['cart_items' => json_encode(['item1' => ['id' => 1, 'qty' => 2]])]);
    $cart->clear();
    $this->assertEmpty($cart->getCartItems());
  }
  /** @test */
  public function it_returns_cart_items_as_array()
  {
    $cart = Cart::factory()->create(['cart_items' => json_encode(['item1' => ['id' => 1, 'qty' => 2]])]);
    $cartItems = $cart->getCartItems();
    $this->assertIsArray($cartItems);
    $this->assertArrayHasKey('item1', $cartItems);
  }
  /** @test */
  public function it_deletes_cart_item()
  {
    $cart = Cart::factory()->create(['cart_items' => json_encode(['item1' => ['id' => 1, 'qty' => 2]])]);
    $cart->deleteCartItem('item1');
    $this->assertArrayNotHasKey('item1', $cart->getCartItems());
  }
  /** @test */
  public function it_saves_cart_item()
  {
    $cart = Cart::factory()->create(['cart_items' => json_encode([])]);
    $cart->saveCart(1, 2);
    $cartItems = $cart->getCartItems();
    $this->assertArrayHasKey(1, $cartItems);
    $this->assertEquals(2, $cartItems[1]['quantity']);
  }
}
