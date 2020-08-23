"""MazaoOnline URL Configuration"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings

from site_models.views import checkout_page, home_page,OrderSummaryView, ProductDetailView,\
    add_to_cart, CheckoutView, PaymentView, remove_single_item_from_cart, remove_from_cart,\
        ContactView, CashDeliveryView
from account.views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_page, name="home_page"),
    path('', home_page, name="home_page"),
    path('product/<slug>/detail/', ProductDetailView.as_view(), name="product"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-product-from-cart/<slug>/', remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('checkout/<int:pk>', checkout_page, name="checkout_page"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('delivery/<str:payment_option>/', CashDeliveryView.as_view(), name="cash-delivery"),
    path('payment/<str:payment_option>/', PaymentView.as_view(), name="payment"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('register/', register_view, name="register_view"),
    path('log_in/', login_view, name="login_view"),
    path('log_out/', logout_view, name="logout_view"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
