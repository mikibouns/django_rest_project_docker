from django.urls import path
from . import views

app_name = 'product_app'

urlpatterns = [
    path('', views.ProductsListViewSet.as_view(), name='product_list'),
    path('<int:art>', views.ProductsDetailViewSet.as_view(), name='product_detail'),
]
