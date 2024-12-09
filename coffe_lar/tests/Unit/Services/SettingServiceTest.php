<?php

namespace Tests\Unit\Services;

use App\Http\Services\SettingService;
use Illuminate\Support\Facades\Cache;
use Tests\TestCase;

class SettingServiceTest extends TestCase
{
  protected function setUp(): void
  {
    parent::setUp();
    // Xóa cache trước mỗi test
    Cache::flush();
  }

  /** @test */
  public function it_can_override_array_values()
  {
    $default = [
      'name' => 'Default Name',
      'email' => 'default@email.com',
      'phone' => '123456'
    ];

    $override = [
      'name' => 'New Name',
      'email' => 'new@email.com'
    ];

    $result = SettingService::array_override($default, $override);

    $this->assertEquals('New Name', $result['name']);
    $this->assertEquals('new@email.com', $result['email']);
    $this->assertEquals('123456', $result['phone']); // Giá trị không bị override giữ nguyên
  }

  /** @test */
  public function it_can_init_settings()
  {
    SettingService::initSetting();

    // Kiểm tra generalSetting được khởi tạo
    $generalSetting = Cache::get('generalSetting');
    $this->assertIsArray($generalSetting);
    $this->assertEquals('Ngôi nhà cafe', $generalSetting['name']);
    $this->assertEquals('Shop', $generalSetting['site_name']);

    // Kiểm tra logoSetting được khởi tạo
    $logoSetting = Cache::get('logoSetting');
    $this->assertIsArray($logoSetting);
    $this->assertArrayHasKey('logo', (array)$logoSetting);
    $this->assertArrayHasKey('favicon', (array)$logoSetting);

    // Kiểm tra emailSetting được khởi tạo
    $emailSetting = Cache::get('emailSetting');
    $this->assertIsArray($emailSetting);
    $this->assertEquals('thanhduy191103@gmail.com', $emailSetting['email']);
  }

  /** @test */
  public function it_can_get_general_setting()
  {
    // Khởi tạo dữ liệu test
    Cache::forever('generalSetting', [
      'name' => 'Test Shop',
      'site_name' => 'Test Site'
    ]);

    $result = SettingService::getGeneralSetting();

    $this->assertIsObject($result);
    $this->assertEquals('Test Shop', $result->name);
    $this->assertEquals('Test Site', $result->site_name);
  }

  /** @test */
  public function it_can_get_email_setting()
  {
    // Khởi tạo dữ liệu test
    Cache::forever('emailSetting', [
      'email' => 'test@email.com',
      'host' => 'smtp.test.com'
    ]);

    $result = SettingService::getEmailSetting();

    $this->assertIsObject($result);
    $this->assertEquals('test@email.com', $result->email);
    $this->assertEquals('smtp.test.com', $result->host);
  }

  /** @test */
  public function it_can_get_logo_setting()
  {
    // Khởi tạo dữ liệu test
    Cache::forever('logoSetting', [
      'logo' => 'logo.png',
      'favicon' => 'favicon.ico'
    ]);

    $result = SettingService::getLogoSetting();

    $this->assertIsObject($result);
    $this->assertEquals('logo.png', $result->logo);
    $this->assertEquals('favicon.ico', $result->favicon);
  }

  /** @test */
  public function it_can_update_general_setting()
  {
    // Khởi tạo cài đặt ban đầu
    SettingService::initSetting();

    // Cập nhật cài đặt
    $updateData = [
      'name' => 'Updated Shop Name',
      'site_name' => 'Updated Site Name'
    ];

    SettingService::updateGeneralSetting($updateData);

    // Kiểm tra cài đặt đã được cập nhật
    $result = SettingService::getGeneralSetting();
    $this->assertEquals('Updated Shop Name', $result->name);
    $this->assertEquals('Updated Site Name', $result->site_name);
  }

  /** @test */
  public function it_can_update_email_setting()
  {
    // Khởi tạo cài đặt ban đầu
    SettingService::initSetting();

    // Cập nhật cài đặt
    $updateData = [
      'email' => 'updated@email.com',
      'host' => 'updated.smtp.com'
    ];

    SettingService::updateEmailSetting($updateData);

    // Kiểm tra cài đặt đã được cập nhật
    $result = SettingService::getEmailSetting();
    $this->assertEquals('updated@email.com', $result->email);
    $this->assertEquals('updated.smtp.com', $result->host);
  }

  /** @test */
  public function it_can_update_logo_setting()
  {
    // Khởi tạo cài đặt ban đầu
    SettingService::initSetting();

    // Cập nhật cài đặt
    $updateData = [
      'logo' => 'new-logo.png',
      'favicon' => 'new-favicon.ico'
    ];

    SettingService::updateLogoSetting($updateData);

    // Kiểm tra cài đặt đã được cập nhật
    $result = SettingService::getLogoSetting();
    $this->assertEquals('new-logo.png', $result->logo);
    $this->assertEquals('new-favicon.ico', $result->favicon);
  }
}
