<?php

namespace Tests;

use App\Models\Role;
use App\Models\User;
use Hash;
use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

/**
 * Những integration test case mà cần người dùng với quyền hạn
 */
abstract class AdminIntegrationTestCase extends IntegrationTestCase
{
    use CreatesApplication;

    protected function setUp(): void
    {
        parent::setUp();
    }

    protected function actingAsAdmin()
    {
        $admin = $this->getAdmin();
        return $this->actingAs($admin);
    }

    protected function getAdmin()
    {
        return User::factory()->create([
            'email' => 'admin@gmail.com',
            'password' => Hash::make('123'),
            ## Add role_id to the factory
            'role_id' => Role::factory()->create()->id,
        ]);
    }
}
