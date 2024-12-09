<?php

namespace Tests\Unit\Requests;

use App\Http\Requests\Auth\LoginRequest;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\ValidationException;
use Tests\TestCase;

class LoginRequestTest extends TestCase
{
    use RefreshDatabase;

    protected $request;

    protected function setUp(): void
    {
        parent::setUp();
        $this->request = new LoginRequest();
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
    public function it_requires_password()
    {
        $validator = Validator::make(
            ['password' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('password', $validator->errors()->messages());
    }

    /** @test */
    public function it_authenticates_user_with_valid_credentials()
    {
        $user = User::factory()->create([
            'email' => 'test@example.com',
            'password' => Hash::make('password123'),
            'status' => true
        ]);

        $request = new LoginRequest();
        $request->merge([
            'email' => 'test@example.com',
            'password' => 'password123'
        ]);

        $result = $request->authenticate();

        $this->assertTrue($result);
        $this->assertTrue(Auth::check());
        $this->assertEquals($user->id, Auth::id());
    }

    /** @test */
    public function it_throws_validation_exception_for_invalid_credentials()
    {
        $user = User::factory()->create([
            'email' => 'test@example.com',
            'password' => Hash::make('password123')
        ]);

        $request = new LoginRequest();
        $request->merge([
            'email' => 'test@example.com',
            'password' => 'wrong_password'
        ]);

        $this->expectException(ValidationException::class);
        $request->authenticate();
    }

    /** @test */
    public function it_throws_validation_exception_for_inactive_user()
    {
        $user = User::factory()->create([
            'email' => 'test@example.com',
            'password' => Hash::make('password123'),
            'status' => false
        ]);

        $request = new LoginRequest();
        $request->merge([
            'email' => 'test@example.com',
            'password' => 'password123'
        ]);

        $this->expectException(ValidationException::class);
        $request->authenticate();
    }

    /** @test */
    public function admin_can_login_regardless_of_status()
    {
        $admin = User::factory()->create([
            'id' => 1,
            'email' => 'admin@example.com',
            'password' => Hash::make('password123'),
            'status' => false
        ]);

        $request = new LoginRequest();
        $request->merge([
            'email' => 'admin@example.com',
            'password' => 'password123'
        ]);

        $result = $request->authenticate();

        $this->assertTrue($result);
        $this->assertTrue(Auth::check());
        $this->assertEquals($admin->id, Auth::id());
    }
} 
