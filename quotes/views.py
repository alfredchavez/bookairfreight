from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from quotes.serializers import (
    ShippingQuotesRequestSerializer,
    ShippingQuotesResponseSerializer,
)
from quotes.utils import (
    QuoteCalculationService,
    Box,
)


class ShippingQuotesView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = ShippingQuotesRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        quotes = QuoteCalculationService.calculate_quotes(
            data["starting_country"],
            data["destination_country"],
            [Box(**box_data) for box_data in data["boxes"]],
        )
        response_serializer = ShippingQuotesResponseSerializer(
            data={"quotes": [quote.model_dump(mode="json") for quote in quotes]}
        )
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data, status=HTTP_200_OK)
