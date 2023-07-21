from django.urls import path
from quotes import views

urlpatterns = [path("", view=views.ShippingQuotesView.as_view())]
