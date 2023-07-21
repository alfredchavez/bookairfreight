import pytest
from pytest_unordered import unordered
from django.forms.models import model_to_dict
from quotes.models import Rate


@pytest.mark.django_db
def test_create_with_weight_rates():
    weights_for_rate1 = [
        {"min_weight_kg": 0, "max_weight_kg": 20, "per_kg_rate": 5.00},
        {"min_weight_kg": 20, "max_weight_kg": 40, "per_kg_rate": 4.50},
        {"min_weight_kg": 40, "max_weight_kg": 100, "per_kg_rate": 4.00},
        {"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 3.50},
    ]
    rate1 = Rate.objects.create_with_weight_rates(
        starting_country="China",
        destination_country="USA",
        shipping_channel="air",
        shipping_time_range_min_days=15,
        shipping_time_range_max_days=20,
        weight_rates=weights_for_rate1,
    )

    weights_for_rate2 = [
        {"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.00}
    ]
    rate2 = Rate.objects.create_with_weight_rates(
        starting_country="China",
        destination_country="USA",
        shipping_channel="ocean",
        shipping_time_range_min_days=45,
        shipping_time_range_max_days=50,
        weight_rates=weights_for_rate2,
    )

    weight_rates1 = rate1.rates.all()
    weight_rates2 = rate2.rates.all()

    weight_rates_as_dict1 = [
        model_to_dict(instance, ["min_weight_kg", "max_weight_kg", "per_kg_rate"])
        for instance in weight_rates1
    ]
    weight_rates_as_dict2 = [
        model_to_dict(instance, ["min_weight_kg", "max_weight_kg", "per_kg_rate"])
        for instance in weight_rates2
    ]

    assert len(weight_rates_as_dict1) == 4
    assert weight_rates_as_dict1 == unordered(weights_for_rate1)
    assert len(weight_rates_as_dict2) == 1
    assert weight_rates_as_dict2 == unordered(weights_for_rate2)
