from django.core.management.base import BaseCommand
from quotes.models import Rate


class Command(BaseCommand):
    help = "Populates the db with predefined data, no extra args needed"

    def _populate_db(self):
        Rate.objects.create_with_weight_rates(
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

        Rate.objects.create_with_weight_rates(
            starting_country="China",
            destination_country="USA",
            shipping_channel="ocean",
            shipping_time_range_min_days=45,
            shipping_time_range_max_days=50,
            weight_rates=[
                {"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.00}
            ],
        )

        Rate.objects.create_with_weight_rates(
            starting_country="India",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=10,
            shipping_time_range_max_days=15,
            weight_rates=[
                {"min_weight_kg": 0, "max_weight_kg": 10, "per_kg_rate": 10.00},
                {"min_weight_kg": 10, "max_weight_kg": 20, "per_kg_rate": 9.50},
                {"min_weight_kg": 20, "max_weight_kg": 30, "per_kg_rate": 9.00},
                {"min_weight_kg": 30, "max_weight_kg": 40, "per_kg_rate": 8.50},
                {"min_weight_kg": 40, "max_weight_kg": 50, "per_kg_rate": 8.00},
                {"min_weight_kg": 50, "max_weight_kg": 10000, "per_kg_rate": 6.00},
            ],
        )

        Rate.objects.create_with_weight_rates(
            starting_country="India",
            destination_country="USA",
            shipping_channel="ocean",
            shipping_time_range_min_days=40,
            shipping_time_range_max_days=50,
            weight_rates=[
                {"min_weight_kg": 100, "max_weight_kg": 10000, "per_kg_rate": 1.50}
            ],
        )

        Rate.objects.create_with_weight_rates(
            starting_country="China",
            destination_country="USA",
            shipping_channel="air",
            shipping_time_range_min_days=15,
            shipping_time_range_max_days=20,
            weight_rates=[
                {"min_weight_kg": 0, "max_weight_kg": 100, "per_kg_rate": 5.00},
                {"min_weight_kg": 100, "max_weight_kg": 200, "per_kg_rate": 4.50},
                {"min_weight_kg": 200, "max_weight_kg": 500, "per_kg_rate": 4.00},
                {"min_weight_kg": 500, "max_weight_kg": 10000, "per_kg_rate": 3.50},
            ],
        )

    def handle(self, *args, **options):
        self._populate_db()
