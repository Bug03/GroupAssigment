<?php

namespace Tests\Unit\Requests;

use App\Http\Requests\Fronend\PaymentRequest;
use Illuminate\Support\Facades\Validator;
use Tests\TestCase;

class PaymentRequestTest extends TestCase
{
    protected $request;

    protected function setUp(): void
    {
        parent::setUp();
        $this->request = new PaymentRequest();
    }

    /** @test */
    public function it_requires_name()
    {
        $validator = Validator::make(
            ['name' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('name', $validator->errors()->messages());
    }

    /** @test */
    public function name_must_not_exceed_255_characters()
    {
        $validator = Validator::make(
            ['name' => str_repeat('a', 256)],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('name', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_email()
    {
        $validator = Validator::make(
            ['email' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('email', $validator->errors()->messages());
    }

    /** @test */
    public function email_must_be_valid()
    {
        $validator = Validator::make(
            ['email' => 'invalid-email'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('email', $validator->errors()->messages());
    }

    /** @test */
    public function phone_must_be_valid_format()
    {
        $validator = Validator::make(
            ['phone' => '123456789'],
            $this->request->rules(),
            $this->request->messages()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('phone', $validator->errors()->messages());
        $this->assertEquals(
            'Số điện thoại chỉ bao gồm 10 số',
            $validator->errors()->first('phone')
        );
    }

    /** @test */
public function phone_accepts_valid_formats()
{
    $validPhones = [
        '0123456789',
        '0987654321',
        '84123456789'
    ];

    foreach ($validPhones as $phone) {
        $validator = Validator::make(
            [
                'name' => 'John Doe',
                'email' => 'john@example.com',
                'phone' => $phone,
                'address' => '123 Main St',
                'province' => 1,
                'district' => 1,
                'ward' => 1
            ],
            $this->request->rules()
        );

        $this->assertFalse($validator->fails(), "Phone number {$phone} should be valid");
    }
}

    /** @test */
    public function it_requires_address()
    {
        $validator = Validator::make(
            ['address' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('address', $validator->errors()->messages());
    }

    /** @test */
    public function address_must_not_exceed_255_characters()
    {
        $validator = Validator::make(
            ['address' => str_repeat('a', 256)],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('address', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_province()
    {
        $validator = Validator::make(
            ['province' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('province', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_district()
    {
        $validator = Validator::make(
            ['district' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('district', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_ward()
    {
        $validator = Validator::make(
            ['ward' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('ward', $validator->errors()->messages());
    }

    /** @test */
    public function it_passes_with_valid_data()
    {
        $validator = Validator::make([
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'phone' => '0123456789',
            'address' => '123 Main St',
            'province' => 1,
            'district' => 1,
            'ward' => 1,
            'note' => 'Some notes'
        ], $this->request->rules());

        $this->assertFalse($validator->fails());
    }
}
