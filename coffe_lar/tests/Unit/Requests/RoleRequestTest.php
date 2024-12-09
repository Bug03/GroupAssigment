<?php

namespace Tests\Unit\Requests;

use App\Http\Requests\Backend\RoleRequest;
use Illuminate\Support\Facades\Validator;
use Tests\TestCase;

class RoleRequestTest extends TestCase
{
    protected $request;

    protected function setUp(): void
    {
        parent::setUp();
        $this->request = new RoleRequest();
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
    public function name_must_not_exceed_200_characters()
    {
        $validator = Validator::make(
            ['name' => str_repeat('a', 201)],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('name', $validator->errors()->messages());
    }

    /** @test */
    public function description_must_not_exceed_200_characters()
    {
        $validator = Validator::make(
            ['description' => str_repeat('a', 201)],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('description', $validator->errors()->messages());
    }

    /** @test */
    public function it_requires_permissions()
    {
        $validator = Validator::make(
            ['permissions' => ''],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('permissions', $validator->errors()->messages());
    }

    /** @test */
    public function permissions_must_be_array()
    {
        $validator = Validator::make(
            ['permissions' => 'not-an-array'],
            $this->request->rules()
        );

        $this->assertTrue($validator->fails());
        $this->assertArrayHasKey('permissions', $validator->errors()->messages());
    }

    /** @test */
    public function it_passes_with_valid_data()
    {
        $validator = Validator::make([
            'name' => 'Admin Role',
            'description' => 'Role for administrators',
            'permissions' => ['create_users', 'edit_users']
        ], $this->request->rules());

        $this->assertFalse($validator->fails());
    }
} 
