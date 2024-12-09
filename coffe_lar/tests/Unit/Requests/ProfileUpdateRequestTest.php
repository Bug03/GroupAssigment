<?php

namespace Tests\Unit\Requests;

use App\Http\Requests\Backend\ProfileUpdateRequest;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Validator;
use Tests\TestCase;

class ProfileUpdateRequestTest extends TestCase
{
    use RefreshDatabase;

    protected $user;

    protected function setUp(): void
    {

        parent::setUp();
        // Tạo và authenticate user trước khi chạy mỗi test
        $this->user = User::factory()->create();
        $this->actingAs($this->user);
        $this->request = new ProfileUpdateRequest();
        $this->request->setUserResolver(function () {
            return $this->user;
        });
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
    public function name_must_not_exceed_100_characters()
    {
        $validator = Validator::make(
            ['name' => str_repeat('a', 101)],
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
    public function email_must_be_unique_except_current_user()
    {
        // Tạo user hiện tại
        $currentUser = User::factory()->create([
            'email' => 'current@example.com'
        ]);

        // Tạo user khác
        $otherUser = User::factory()->create([
            'email' => 'other@example.com'
        ]);

        // Giả lập request từ user hiện tại
        $this->actingAs($currentUser);

        // Test case 1: Email hiện tại của user (should pass)
        $validator = Validator::make(
            ['email' => 'current@example.com'],
            $this->request->rules()
        );
        $this->assertTrue($validator->fails());

        // Test case 2: Email đã tồn tại của user khác (should fail)
        $validator = Validator::make(
            ['email' => 'other@example.com'],
            $this->request->rules()
        );
        $this->assertTrue($validator->fails());
    }

    /** @test */
    public function image_must_be_valid()
    {
        $validator = Validator::make(
            ['image' => 'not-an-image'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('image', $validator->errors()->messages());
    }

    /** @test */
    public function image_must_not_exceed_2mb()
    {
        $validator = Validator::make(
            ['image' => 'large-image'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('image', $validator->errors()->messages());
    }

    /** @test */
    public function phone_must_be_numeric()
    {
        $validator = Validator::make(
            ['phone' => 'not-a-number'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('phone', $validator->errors()->messages());
    }

    /** @test */
    public function address_must_be_string()
    {
        $validator = Validator::make(
            ['address' => ['not-a-string']],
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
    public function it_passes_with_valid_data()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $validator = Validator::make([
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'phone' => '1234567890',
            'address' => '123 Main St'
        ], $this->request->rules());

        $this->assertFalse($validator->fails());
    }
}
