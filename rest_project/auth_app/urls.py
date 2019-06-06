from django.urls import path
from . import views

app_name = 'auth_app'


urlpatterns = [
    path('', views.UserListViewSet.as_view(), name='user_list'),
    path('<int:pk>/', views.UserDetailViewSet.as_view(), name='user_detail'),

]
