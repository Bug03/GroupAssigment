<?php

namespace Tests\Unit\Models;

use Tests\TestCase;
use App\Models\Permission;
use App\Models\Role;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Database\Eloquent\Collection;

class PermissionTest extends TestCase
{
    use RefreshDatabase;

    protected Permission $permission;

    protected function setUp(): void
    {
        parent::setUp();
        $this->permission = Permission::factory()->create([
            'name' => 'test-permission',
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
        $this->assertEquals($expectedFillable, $this->permission->getFillable());
    }

    /** @test */
    public function it_belongs_to_many_roles()
    {
        // Arrange
        $role = Role::factory()->create();
        $this->permission->roles()->attach($role->id);

        // Assert
        $this->assertInstanceOf(Collection::class, $this->permission->roles);
        $this->assertTrue($this->permission->roles->contains($role));
    }

    /** @test */
    public function it_can_attach_and_detach_roles()
    {
        // Arrange
        $roles = Role::factory()->count(2)->create();

        // Act - Attach
        $this->permission->roles()->attach($roles->pluck('id'));

        // Assert
        $this->assertEquals(2, $this->permission->roles()->count());

        // Act - Detach
        $this->permission->roles()->detach($roles->first()->id);

        // Assert
        $this->assertEquals(1, $this->permission->roles()->count());
    }

    /** @test */
    public function it_can_sync_roles()
    {
        // Arrange
        $roles = Role::factory()->count(3)->create();

        // Act
        $this->permission->roles()->sync($roles->pluck('id'));

        // Assert
        $this->assertEquals(3, $this->permission->roles()->count());

        // Act - Sync with new set
        $newRoles = Role::factory()->count(2)->create();
        $this->permission->roles()->sync($newRoles->pluck('id'));

        // Assert
        $this->assertEquals(2, $this->permission->roles()->count());
    }

    /** @test */
    public function it_can_get_and_set_name()
    {
        // Assert - Get
        $this->assertEquals('test-permission', $this->permission->name);

        // Act - Set
        $this->permission->name = 'new-permission';
        $this->permission->save();

        // Assert
        $this->assertEquals('new-permission', $this->permission->fresh()->name);
    }

    /** @test */
    public function it_can_get_and_set_description()
    {
        // Assert - Get
        $this->assertEquals('Test Description', $this->permission->description);

        // Act - Set
        $this->permission->description = 'New Description';
        $this->permission->save();

        // Assert
        $this->assertEquals('New Description', $this->permission->fresh()->description);
    }

    /** @test */
    public function it_can_create_permission()
    {
        // Arrange
        $permissionData = [
            'name' => 'create-users',
            'description' => 'Can create users'
        ];

        // Act
        $newPermission = Permission::create($permissionData);

        // Assert
        $this->assertInstanceOf(Permission::class, $newPermission);
        $this->assertDatabaseHas('permissions', $permissionData);
    }

    /** @test */
    public function it_can_update_permission()
    {
        // Arrange
        $updateData = [
            'name' => 'updated-permission',
            'description' => 'Updated description'
        ];

        // Act
        $this->permission->update($updateData);

        // Assert
        $this->assertDatabaseHas('permissions', $updateData);
    }

    /** @test */
    public function it_can_delete_permission()
    {
        // Arrange
        $permissionId = $this->permission->id;

        // Act
        $this->permission->delete();

        // Assert
        $this->assertDatabaseMissing('permissions', ['id' => $permissionId]);
    }
}
