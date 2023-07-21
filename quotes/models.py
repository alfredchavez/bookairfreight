from django.db import models
from quotes.managers import RateManager


class Rate(models.Model):
    starting_country = models.CharField(max_length=255)
    destination_country = models.CharField(max_length=255)
    shipping_channel = models.CharField(max_length=255)
    shipping_time_range_min_days = models.IntegerField()
    shipping_time_range_max_days = models.IntegerField()

    objects = RateManager()


class PerWeightRate(models.Model):
    min_weight_kg = models.FloatField()
    max_weight_kg = models.FloatField()
    per_kg_rate = models.FloatField()
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, related_name="rates")
