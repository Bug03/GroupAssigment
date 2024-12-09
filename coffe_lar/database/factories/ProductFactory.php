<?php

namespace Database\Factories;

use App\Models\Category;
use App\Models\Product;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class ProductFactory extends Factory
{
    protected $model = Product::class;

    public function definition()
    {
        return [
            'name' => $this->faker->word,
            'slug' => function (array $attributes) {
                return Str::slug($attributes['name']);
            },
            'category_id' => Category::factory(),
            'thumb_image' => $this->faker->imageUrl(),
            'description' => $this->faker->sentence,
            'content' => $this->faker->paragraph,
            'price' => $this->faker->numberBetween(10000, 1000000),
            'weight' => $this->faker->numberBetween(100, 1000),
            'status' => true
        ];
    }
}
