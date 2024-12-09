<?php

namespace Tests\Unit\Requests;

use App\Http\Requests\Fronend\CartRequest;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Validator;
use Tests\TestCase;

class CartRequestTest extends TestCase
{
    use RefreshDatabase;

    protected $request;

    protected function setUp(): void
    {
        parent::setUp();
        $this->request = new CartRequest();
    }

    /** @test */
    public function unauthorized_users_cannot_access()
    {
        $this->assertFalse($this->request->authorize());
    }

    /** @test */
    public function authorized_users_can_access()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $this->assertTrue($this->request->authorize());
    }

    /** @test */
    public function it_requires_quantity()
    {
        $validator = Validator::make(
            ['qty' => ''],
            $this->request->rules(),
            $this->request->messages(),
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('qty', $validator->errors()->messages());
        $this->assertEquals(
            'Bạn cần nhập số lượng và phải là số',
            $validator->errors()->first('qty')
        );
    }

    /** @test */
    public function quantity_must_be_integer()
    {
        $validator = Validator::make(
            ['qty' => 'not-a-number'],
            $this->request->rules(),
            $this->request->messages(),
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('qty', $validator->errors()->messages());
        $this->assertEquals(
            'Số lượng phải là số',
            $validator->errors()->first('qty')
        );
    }

    /** @test */
    public function quantity_must_be_at_least_one()
    {
        $validator = Validator::make(
            ['qty' => 0],
            $this->request->rules(),
            $this->request->messages(),
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('qty', $validator->errors()->messages());
        $this->assertEquals(
            'Số lượng sản phẩm phải lớn hơn 0',
            $validator->errors()->first('qty')
        );
    }

    /** @test */
    public function variants_items_must_be_array()
    {
        $validator = Validator::make(
            ['variants_items' => 'not-an-array'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('variants_items', $validator->errors()->messages());
    }

    /** @test */
    public function it_passes_with_valid_data()
    {
        $validator = Validator::make([
            'qty' => 1,
            'variants_items' => ['size' => 'L', 'color' => 'red']
        ], $this->request->rules());

        $this->assertFalse($validator->fails());
    }
}
