<?php

namespace Tests\Unit\Models;

use Tests\TestCase;
use App\Models\Role;
use App\Models\User;
use App\Models\Permission;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Database\Eloquent\Collection;

class RoleTest extends TestCase
{
    use RefreshDatabase;

    protected Role $role;

    protected function setUp(): void
    {
        parent::setUp();
        $this->role = Role::factory()->create([
            'name' => 'test-role',
            'description' => 'Test Description'
        ]);
    }

    /** @test */
    public function it_has_correct_fillable_attributes()
    {
        // Arrange
        $expectedFillable = [
            'name',
            'description',
        ];

        // Assert
        $this->assertEquals($expectedFillable, $this->role->getFillable());
    }

    /** @test */
    public function it_has_many_users()
    {
        // Arrange
        $user = User::factory()->create(['role_id' => $this->role->id]);

        // Assert
        $this->assertInstanceOf(Collection::class, $this->role->users);
        $this->assertTrue($this->role->users->contains($user));
    }

    /** @test */
    public function it_belongs_to_many_permissions()
    {
        // Arrange
        $permission = Permission::factory()->create();
        $this->role->permissions()->attach($permission->id);

        // Assert
        $this->assertInstanceOf(Collection::class, $this->role->permissions);
        $this->assertTrue($this->role->permissions->contains($permission));
    }

    /** @test */
    public function it_can_get_and_set_name()
    {
        // Assert - Get
        $this->assertEquals('test-role', $this->role->name);

        // Act - Set
        $this->role->name = 'new-role';
        $this->role->save();

        // Assert
        $this->assertEquals('new-role', $this->role->fresh()->name);
    }

    /** @test */
    public function it_can_get_and_set_description()
    {
        // Assert - Get
        $this->assertEquals('Test Description', $this->role->description);

        // Act - Set
        $this->role->description = 'New Description';
        $this->role->save();

        // Assert
        $this->assertEquals('New Description', $this->role->fresh()->description);
    }

    /** @test */
    public function it_can_create_role()
    {
        // Arrange
        $roleData = [
            'name' => 'admin',
            'description' => 'Administrator role'
        ];

        // Act
        $newRole = Role::create($roleData);

        // Assert
        $this->assertInstanceOf(Role::class, $newRole);
        $this->assertDatabaseHas('roles', $roleData);
    }

    /** @test */
    public function it_can_update_role()
    {
        // Arrange
        $updateData = [
            'name' => 'updated-role',
            'description' => 'Updated description'
        ];

        // Act
        $this->role->update($updateData);

        // Assert
        $this->assertDatabaseHas('roles', $updateData);
    }

    /** @test */
    public function it_can_delete_role()
    {
        // Arrange
        $roleId = $this->role->id;

        // Act
        $this->role->delete();

        // Assert
        $this->assertDatabaseMissing('roles', ['id' => $roleId]);
    }

    /** @test */
    public function it_can_attach_and_detach_permissions()
    {
        // Arrange
        $permissions = Permission::factory()->count(2)->create();

        // Act - Attach
        $this->role->permissions()->attach($permissions->pluck('id')->toArray());

        // Assert
        $this->role->refresh();
        $this->assertEquals(2, $this->role->permissions()->count());

        // Act - Detach
        $this->role->permissions()->detach($permissions->first()->id);

        // Assert
        $this->role->refresh();
        $this->assertEquals(1, $this->role->permissions()->count());
    }

    /** @test */
    public function it_can_sync_permissions()
    {
        // Arrange
        $permissions = Permission::factory()->count(3)->create();

        // Act
        $this->role->permissions()->sync($permissions->pluck('id')->toArray());

        // Assert
        $this->role->refresh();
        $this->assertEquals(3, $this->role->permissions()->count());

        // Act - Sync with new set
        $newPermissions = Permission::factory()->count(2)->create();
        $this->role->permissions()->sync($newPermissions->pluck('id')->toArray());

        // Assert
        $this->role->refresh();
        $this->assertEquals(2, $this->role->permissions()->count());
    }
} 
