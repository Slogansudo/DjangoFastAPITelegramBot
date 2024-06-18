from django.urls import path
from .views import ShopView, AboutUsView, ServicesView, BlogsView, ContactUsView, ShopDetailView, CartDetailView, CheckoutView

urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('shop/<int:id>/', ShopDetailView.as_view(), name='shop-detail'),
    path("cart/", CartDetailView.as_view(), name='cart'),
    path("checkout/", CheckoutView.as_view(), name='checkout')
]
