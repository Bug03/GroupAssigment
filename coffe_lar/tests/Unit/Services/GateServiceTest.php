<?php

namespace Tests\Unit\Services;

use App\Http\Services\GateService;
use Tests\TestCase;

class GateServiceTest extends TestCase
{
  /** @test */
  public function it_can_get_gate_define_from_route_name_with_index()
  {
    // Test với route có đuôi index
    $routeName = 'admin.category.index';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('admin.category', $result);
  }

  /** @test */
  public function it_can_get_gate_define_from_route_name_with_create()
  {
    // Test với route có đuôi create
    $routeName = 'admin.product.create';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('admin.product', $result);
  }

  /** @test */
  public function it_can_get_gate_define_from_route_name_with_edit()
  {
    // Test với route có đuôi edit
    $routeName = 'admin.user.edit';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('admin.user', $result);
  }

  /** @test */
  public function it_can_get_gate_define_from_route_name_with_change_status()
  {
    // Test với route có đuôi change-status
    $routeName = 'admin.order.change-status';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('admin.order', $result);
  }

  /** @test */
  public function it_can_get_gate_define_from_single_segment_route()
  {
    // Test với route chỉ có một phần
    $routeName = 'dashboard';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('', $result);
  }

  /** @test */
  public function it_can_get_gate_define_from_empty_route()
  {
    // Test với route rỗng
    $routeName = '';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('', $result);
  }

  /** @test */
  public function it_can_get_gate_define_from_route_without_dot()
  {
    // Test với route không có dấu chấm
    $routeName = 'adminuseredit';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('', $result);
  }

  /** @test */
  public function it_can_get_gate_define_from_multiple_dots_route()
  {
    // Test với route có nhiều dấu chấm
    $routeName = 'admin.user.profile.edit';
    $result = GateService::getGateDefineFromRouteName($routeName);

    $this->assertEquals('admin.user.profile', $result);
  }
}
