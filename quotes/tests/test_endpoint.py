from rest_framework.test import APIClient
import pytest
from quotes.models import Rate


@pytest.mark.django_db
def test_calculate_quotes_no_results():
    rate1 = Rate.objects.create_with_weight_rates(
        starting_country="China",
        destination_country="USA",
        shipping_channel="air",
        shipping_time_range_min_days=15,
        shipping_time_range_max_days=20,
        weight_rates=[
            {"min_weight_kg": 0, "max_weight_kg": 20, "per_kg_rate": 5.00},
            {"min_weight_kg": 20, "max_weight_kg": 40, "per_kg_rate": 4.50},
            {"min_weight_kg": 40, "max_weight_kg": 100, "per_kg_rate": 4.00},
            {"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 3.50},
        ],
    )
    expected_response = {
        "quotes": [
            {
                "shipping_channel": "air",
                "total_cost": 7400.0,
                "cost_breakdown": {
                    "shipping_cost": 7000.0,
                    "service_fee": 300.0,
                    "oversized_fee": 100.0,
                    "overweight_fee": 0.0,
                },
                "shipping_time_range": {"min_days": 15, "max_days": 20},
            },
        ]
    }
    client = APIClient()
    response = client.post(
        "/v1/quotes",
        {
            "starting_country": "China",
            "destination_country": "USA",
            "boxes": [
                {
                    "count": 100,
                    "weight_kg": 10,
                    "length": 200,
                    "width": 20,
                    "height": 30,
                }
            ],
        },
        format="json",
    )
    assert response.status_code == 200
    assert response.data == expected_response
