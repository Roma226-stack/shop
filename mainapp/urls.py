import debug_toolbar
from django.urls import path
from mainapp.views import (ProductDetailView,
                           CategoryDetailView,
                           BaseView,
                           CheckoutView,
                           AddToCartView,
                           DeleteFromCartView,
                           ChangeQTYView,
                           CartView,)
                           # Login,
                           # Logout,)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:ct_model>/<str:slug>', ChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('accounts/login/', Login.as_view(), name='login'),
    # path('accounts/logout/', Logout.as_view(), name='logout'),
    # path('api-auth/', include('rest_framework.urls'))
]
