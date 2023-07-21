from rest_framework import serializers


class BoxSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    weight_kg = serializers.FloatField()
    length = serializers.FloatField()
    width = serializers.FloatField()
    height = serializers.FloatField()


class ShippingQuotesRequestSerializer(serializers.Serializer):
    starting_country = serializers.CharField()
    destination_country = serializers.CharField()
    boxes = BoxSerializer(many=True)


class CostBreakdownSerializer(serializers.Serializer):
    shipping_cost = serializers.FloatField()
    service_fee = serializers.FloatField()
    oversized_fee = serializers.FloatField()
    overweight_fee = serializers.FloatField()


class ShippingTimeRangeSerializer(serializers.Serializer):
    min_days = serializers.IntegerField()
    max_days = serializers.IntegerField()


class QuoteSerializer(serializers.Serializer):
    shipping_channel = serializers.CharField()
    total_cost = serializers.FloatField()
    cost_breakdown = CostBreakdownSerializer()
    shipping_time_range = ShippingTimeRangeSerializer()


class ShippingQuotesResponseSerializer(serializers.Serializer):
    quotes = QuoteSerializer(many=True)
