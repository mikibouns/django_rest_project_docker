from django.urls import path
from . import views

app_name = 'basket_app'

urlpatterns = [
    path('', views.BasketListViewSet.as_view(), name='basket_list'),
    path('<int:pk>/', views.BasketDetailViewSet.as_view(), name='basket_detail'),
    path('<int:pk>/<int:prod>', views.BasketDeleteViewSet.as_view(), name='purchase_detail'),
]
