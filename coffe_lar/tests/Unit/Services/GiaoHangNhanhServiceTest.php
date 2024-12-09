<?php

namespace Tests\Unit\Services;

use App\Http\Services\GiaoHangNhanhService;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class GiaoHangNhanhServiceTest extends TestCase
{
    protected $ghnService;

    protected function setUp(): void
    {
        parent::setUp();
        $this->ghnService = new GiaoHangNhanhService();
    }

    /** @test */
    public function it_gets_provinces_list()
    {
        // Arrange
        $url = 'https://online-gateway.ghn.vn/shiip/public-api/master-data/province';
        $nameCache = 'province';

        // Act
        $response = Http::withHeaders([
            'token' => env('TOKEN_GHN'),
            'Content-Type' => 'application/json'
        ])->get($url);

        // Debug
        // dump("Response từ API Provinces:");
        // dump($response->json());

        // Assert
        $this->assertTrue($response->successful());
        $this->assertArrayHasKey('data', $response->json());
    }

    /** @test */
    public function it_gets_districts_by_province()
    {
        // Arrange
        $provinceId = 202; // Mã tỉnh HCM
        $url = 'https://online-gateway.ghn.vn/shiip/public-api/master-data/district';
        $nameCache = 'district-' . $provinceId;
        $params = ['province_id' => $provinceId];

        // Act
        $response = Http::withHeaders([
            'token' => env('TOKEN_GHN'),
            'Content-Type' => 'application/json'
        ])->get($url, $params);

        // // Debug
        // dump("Response từ API Districts của HCM:");
        // dump($response->json());

        // Assert
        $this->assertTrue($response->successful());
        $this->assertArrayHasKey('data', $response->json());
    }

    /** @test */
    public function it_gets_wards_by_district()
    {
        // Arrange
        $districtId = 1442; // Mã Quận 1
        $url = 'https://online-gateway.ghn.vn/shiip/public-api/master-data/ward';
        $nameCache = 'ward-' . $districtId;
        $params = ['district_id' => $districtId];

        // Act
        $response = Http::withHeaders([
            'token' => env('TOKEN_GHN'),
            'Content-Type' => 'application/json'
        ])->get($url, $params);

        // Debug
        // dump("Response từ API Wards của Quận 1:");
        // dump($response->json());

        // Assert
        $this->assertTrue($response->successful());
        $this->assertArrayHasKey('data', $response->json());
    }

    /**
    * Provide test cases for shipping fee calculation
    * @return array
    */
    public function shippingFeeProvider(): array
    {
        return [
            'Giao hàng Quận 1 - 1kg' => [
                1442,      // district_id - Quận 1
                "20109",   // ward_code - Phường Đa Kao
                1000,      // weight - 1kg
                2         // service_type_id (giao hàng nhanh)
            ],
            'Giao hàng Quận 2 - 2kg' => [
                1443,      // district_id - Quận 2
                "20208",   // ward_code - Phường An Phú
                2000,      // weight - 2kg
                2
            ],
            'Giao hàng Quận Bình Thạnh - 500g' => [
                1467,      // district_id - Quận Bình Thạnh
                "20308",   // ward_code - Phường 1
                500,       // weight - 500g
                2
            ],
            'Giao hàng Quận 7 - 3kg' => [
                1459,      // district_id - Quận 7
                "20408",   // ward_code - Phường Tân Thuận Đông
                3000,      // weight - 3kg
                2
            ],
            'Giao hàng Quận Thủ Đức - 5kg' => [
                1451,      // district_id - Quận Thủ Đức
                "20508",   // ward_code - Phường Linh Trung
                5000,      // weight - 5kg
                2
            ]
        ];
    }

    /**
    * Test shipping fee calculation with different parameters
    *
    * @test
    * @dataProvider shippingFeeProvider
    * @param int $districtId District ID
    * @param string $wardCode Ward Code
    * @param int $weight Weight in grams
    * @param int $serviceTypeId Service Type ID
    */
    public function it_calculates_shipping_fee(
        int $districtId,
        string $wardCode,
        int $weight,
        int $serviceTypeId
    ) {
        // Arrange
        $url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee';
        $nameCache = "ward-{$districtId}service-{$wardCode}";
        $params = [
            'shop_id' => env('GHN_SHOP_ID', 4579088),
            'service_type_id' => $serviceTypeId,
            'to_district_id' => $districtId,
            'to_ward_code' => $wardCode,
            'weight' => $weight,
        ];

        // Act
        $response = Http::withHeaders([
            'token' => env('TOKEN_GHN'),
            'Content-Type' => 'application/json'
        ])->post($url, $params);

        // Debug
        // dump("\n----- Test case: Quận {$districtId} - {$weight}g -----");
        // dump("Request params:");
        // dump($params);
        // dump("Response từ API:");
        // dump($response->json());

        if ($response->successful()) {
            $price = $response->json()['data']['total'] ?? null;
            dump("Giá ship: " . ($price ? number_format($price, 0, ',', '.') . " VNĐ" : "Không lấy được giá"));
        }

        // Assert
        $this->assertTrue($response->successful(), "API call failed for District {$districtId}");
        $this->assertArrayHasKey('data', $response->json(), "Missing data key for District {$districtId}");
        $this->assertArrayHasKey('total', $response->json()['data'], "Missing total key for District {$districtId}");
        $this->assertIsNumeric($response->json()['data']['total'], "Invalid total value for District {$districtId}");
    }



    /** @test */
    public function it_handles_api_errors()
    {
        // Arrange
        $url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee';
        $nameCache = 'error-test';
        $params = [
            'shop_id' => env('GHN_SHOP_ID', 4579088),
            'service_type_id' => 2,
            'to_district_id' => 99999,     // Invalid district
            'to_ward_code' => "99999",     // Invalid ward
            'weight' => 1000,
        ];

        // Act
        $response = Http::withHeaders([
            'token' => env('TOKEN_GHN'),
            'Content-Type' => 'application/json'
        ])->post($url, $params);

        // Debug
        // dump("Response từ API với params không hợp lệ:");
        // dump($response->json());

        // Assert
        $this->assertFalse($response->successful());
    }
}
