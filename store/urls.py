from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('cart/', views.cart, name="cart"),
    path('store/', views.store, name="store"),
    path('checkout/', views.Checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name='process_order'),
    path('product-search/', views.productSearch, name='product_search'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"), name="password_reset_complete"),
    path('mens-clothing/', views.mens_clothing_list, name='mens_clothing_list'),
    path('mens-clothing/<int:item_id>/', views.view_clothing_detail, name='view_clothing_detail'),
    path('womens-clothing/', views.womens_clothing_list, name='womens_clothing_list'),
    path('kids-clothing/', views.kids_clothing_list, name='kids_clothing_list'),
]

