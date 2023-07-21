import functools
from quotes.models import PerWeightRate
from pydantic import BaseModel, computed_field


class Box(BaseModel):
    count: int
    weight_kg: float
    length: float
    width: float
    height: float

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height

    @property
    def longest_dimension(self) -> float:
        return max(self.length, self.width, self.height)


class QuotePriceBreakdown(BaseModel):
    shipping_cost: float
    service_fee: float
    oversized_fee: float
    overweight_fee: float


class ShippingTimeRange(BaseModel):
    min_days: int
    max_days: int


class Quote(BaseModel):
    shipping_channel: str
    cost_breakdown: QuotePriceBreakdown
    shipping_time_range: ShippingTimeRange

    @computed_field
    @property
    def total_cost(self) -> float:
        return (
            self.cost_breakdown.shipping_cost
            + self.cost_breakdown.service_fee
            + self.cost_breakdown.overweight_fee
            + self.cost_breakdown.oversized_fee
        )


class QuoteCalculationService:
    @staticmethod
    def _calculate_gross_weight(boxes: list[Box]):
        return functools.reduce(
            lambda gross_weight, box: gross_weight + box.count * box.weight_kg, boxes, 0
        )

    @staticmethod
    def _calculate_volumetric_weight(boxes: list[Box]):
        print("calculate volumetric")
        return functools.reduce(
            lambda vol_weight, box: vol_weight + (box.count * box.volume / 6000),
            boxes,
            0,
        )

    @staticmethod
    def _is_box_overweight(starting_country: str, box: Box) -> bool:
        if starting_country == "India":
            return box.weight_kg >= 15
        return box.weight_kg > 30

    @staticmethod
    def _is_box_oversized(starting_country: str, box: Box) -> bool:
        if starting_country == "Vietnam":
            return box.longest_dimension > 70
        return box.longest_dimension > 120

    @staticmethod
    def _calculate_boxes_overweight_fee(
        starting_country: str, boxes: list[Box]
    ) -> float:
        return functools.reduce(
            lambda fee, box: fee + 80
            if QuoteCalculationService._is_box_overweight(starting_country, box)
            else 0,
            boxes,
            0,
        )

    @staticmethod
    def _calculate_boxes_oversized_fee(
        starting_country: str, boxes: list[Box]
    ) -> float:
        return functools.reduce(
            lambda fee, box: fee + 100
            if QuoteCalculationService._is_box_oversized(starting_country, box)
            else 0,
            boxes,
            0,
        )

    @staticmethod
    def _calculate_service_fee(starting_country: str) -> float:
        return 300 if starting_country == "China" else 0

    @staticmethod
    def calculate_quotes(
        starting_country: str, destination_country: str, boxes: list[Box]
    ) -> list[Quote]:
        chargeable_weight = max(
            QuoteCalculationService._calculate_gross_weight(boxes),
            QuoteCalculationService._calculate_volumetric_weight(boxes),
        )
        rates_for_weight = PerWeightRate.objects.filter(
            rate__starting_country=starting_country,
            rate__destination_country=destination_country,
            min_weight_kg__lte=chargeable_weight,
            max_weight_kg__gte=chargeable_weight,
        )
        return [
            Quote(
                shipping_channel=rate.rate.shipping_channel,
                cost_breakdown=QuotePriceBreakdown(
                    shipping_cost=round(chargeable_weight * rate.per_kg_rate, 2),
                    service_fee=round(
                        QuoteCalculationService._calculate_service_fee(
                            starting_country
                        ),
                        2,
                    ),
                    oversized_fee=round(
                        QuoteCalculationService._calculate_boxes_oversized_fee(
                            starting_country, boxes
                        ),
                        2,
                    ),
                    overweight_fee=round(
                        QuoteCalculationService._calculate_boxes_overweight_fee(
                            starting_country, boxes
                        ),
                        2,
                    ),
                ),
                shipping_time_range=ShippingTimeRange(
                    min_days=rate.rate.shipping_time_range_min_days,
                    max_days=rate.rate.shipping_time_range_max_days,
                ),
            )
            for rate in rates_for_weight
        ]
