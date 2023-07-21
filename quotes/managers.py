from django.db import models
from django.apps import apps


class RateManager(models.Manager):
    def create_with_weight_rates(
        self,
        starting_country: str,
        destination_country: str,
        shipping_channel: str,
        shipping_time_range_min_days: int,
        shipping_time_range_max_days: int,
        weight_rates: list[dict[str, str]],
    ):
        rate = self.model(
            starting_country=starting_country,
            destination_country=destination_country,
            shipping_channel=shipping_channel,
            shipping_time_range_min_days=shipping_time_range_min_days,
            shipping_time_range_max_days=shipping_time_range_max_days,
        )
        rate.save()

        per_weight_rate_model = apps.get_model("quotes", "PerWeightRate")

        per_weight_rate_model.objects.bulk_create(
            [
                per_weight_rate_model(
                    min_weight_kg=weight_rate["min_weight_kg"],
                    max_weight_kg=weight_rate["max_weight_kg"],
                    per_kg_rate=weight_rate["per_kg_rate"],
                    rate_id=rate.id,
                )
                for weight_rate in weight_rates
            ]
        )
        return rate
