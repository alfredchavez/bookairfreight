import pytest
from model_bakery.recipe import Recipe, foreign_key
from quotes.utils import (
    QuoteCalculationService,
    Box,
    Quote,
    QuotePriceBreakdown,
    ShippingTimeRange,
)

INITIAL_DB_DATA = [
    {
        "starting_country": "China",
        "destination_country": "USA",
        "shipping_channel": "air",
        "shipping_time_range": {"min_days": 15, "max_days": 20},
        "rates": [
            {"min_weight_kg": 0, "max_weight_kg": 20, "per_kg_rate": 5.00},
            {"min_weight_kg": 20, "max_weight_kg": 40, "per_kg_rate": 4.50},
            {"min_weight_kg": 40, "max_weight_kg": 100, "per_kg_rate": 4.00},
            {"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 3.50},
        ],
    },
    {
        "starting_country": "China",
        "destination_country": "USA",
        "shipping_channel": "ocean",
        "shipping_time_range": {"min_days": 45, "max_days": 50},
        "rates": [{"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.00}],
    },
    {
        "starting_country": "India",
        "destination_country": "USA",
        "shipping_channel": "air",
        "shipping_time_range": {"min_days": 10, "max_days": 15},
        "rates": [
            {"min_weight_kg": 0, "max_weight_kg": 10, "per_kg_rate": 10.00},
            {"min_weight_kg": 10, "max_weight_kg": 20, "per_kg_rate": 9.50},
            {"min_weight_kg": 20, "max_weight_kg": 30, "per_kg_rate": 9.00},
            {"min_weight_kg": 30, "max_weight_kg": 40, "per_kg_rate": 8.50},
            {"min_weight_kg": 40, "max_weight_kg": 50, "per_kg_rate": 8.00},
            {"min_weight_kg": 50, "max_weight_kg": 10000, "per_kg_rate": 6.00},
        ],
    },
    {
        "starting_country": "India",
        "destination_country": "USA",
        "shipping_channel": "ocean",
        "shipping_time_range": {"min_days": 40, "max_days": 50},
        "rates": [{"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.50}],
    },
    {
        "starting_country": "Vietnam",
        "destination_country": "USA",
        "shipping_channel": "air",
        "shipping_time_range": {"min_days": 0, "max_days": 100},
        "rates": [
            {"min_weight_kg": 0, "max_weight_kg": 100, "per_kg_rate": 5.00},
            {"min_weight_kg": 100, "max_weight_kg": 200, "per_kg_rate": 4.50},
            {"min_weight_kg": 200, "max_weight_kg": 500, "per_kg_rate": 4.00},
            {"min_weight_kg": 500, "max_weight_kg": 10000, "per_kg_rate": 3.50},
        ],
    },
]


class TestQuoteCalculationService:
    @pytest.mark.django_db
    def test_calculate_quotes_from_china(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="China",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=2,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=10, length=200, width=100, height=20),
            Box(count=2, weight_kg=10, length=210, width=110, height=30),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=3036.20,
                service_fee=300,
                oversized_fee=200,
                overweight_fee=0,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=2,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "China",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_oversized_from_vietnam(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="Vietnam",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=2,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=10, length=20, width=10, height=20),
            Box(count=2, weight_kg=10, length=21, width=11, height=80),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=306,
                service_fee=0,
                oversized_fee=100,
                overweight_fee=0,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=2,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "Vietnam",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_standard_from_vietnam(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="Vietnam",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=2,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=10, length=20, width=10, height=20),
            Box(count=2, weight_kg=10, length=21, width=11, height=50),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=306,
                service_fee=0,
                oversized_fee=0,
                overweight_fee=0,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=2,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "Vietnam",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_oversized(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="Peru",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=2,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=10, length=20, width=10, height=20),
            Box(count=2, weight_kg=10, length=21, width=11, height=150),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=306,
                service_fee=0,
                oversized_fee=100,
                overweight_fee=0,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=2,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "Peru",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_overweight(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="Peru",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=2,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=50, length=20, width=10, height=20),
            Box(count=2, weight_kg=60, length=21, width=11, height=100),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=1734,
                service_fee=0,
                oversized_fee=0,
                overweight_fee=160,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=2,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "Peru",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_oversized_and_overweight(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="Peru",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=2,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=50, length=20, width=10, height=200),
            Box(count=2, weight_kg=60, length=21, width=11, height=150),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=1734,
                service_fee=0,
                oversized_fee=200,
                overweight_fee=160,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=2,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "Peru",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_standard_from_india(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="India",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=2,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=12, length=20, width=10, height=50),
            Box(count=2, weight_kg=13, length=21, width=11, height=50),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=387.6,
                service_fee=0,
                oversized_fee=0,
                overweight_fee=0,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=2,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "India",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_overweight_from_india(self, mocker):
        rate = Recipe(
            "quotes.Rate",
            starting_country="India",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=1,
            shipping_time_range_max_days=4,
        )

        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[
                Recipe(
                    "quotes.PerWeightRate",
                    min_weight_kg=10,
                    max_weight_kg=2000,
                    per_kg_rate=10.2,
                    rate=foreign_key(rate),
                ).make()
            ],
        )

        test_boxes = [
            Box(count=1, weight_kg=20, length=20, width=10, height=50),
            Box(count=2, weight_kg=30, length=21, width=11, height=50),
        ]

        expected_quote = Quote(
            shipping_channel="air",
            cost_breakdown=QuotePriceBreakdown(
                shipping_cost=816,
                service_fee=0,
                oversized_fee=0,
                overweight_fee=160,
            ),
            shipping_time_range=ShippingTimeRange(
                min_days=1,
                max_days=4,
            ),
        )

        quotes = QuoteCalculationService.calculate_quotes(
            "India",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 1
        assert quotes[0].model_dump(mode="json") == expected_quote.model_dump(
            mode="json"
        )

    @pytest.mark.django_db
    def test_calculate_quotes_no_results(self, mocker):
        mocker.patch(
            "quotes.models.PerWeightRate.objects.filter",
            return_value=[],
        )

        test_boxes = [
            Box(count=1, weight_kg=290, length=20, width=10, height=50),
            Box(count=2, weight_kg=390, length=21, width=11, height=50),
        ]

        quotes = QuoteCalculationService.calculate_quotes(
            "India",
            "USA",
            test_boxes,
        )
        assert len(quotes) == 0
