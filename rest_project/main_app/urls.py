from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='API')


app_name = 'main_app'

urlpatterns = [
    path('', views.APIRootView.as_view(), name='main_app'),
    path('swagger_api_docs/', schema_view, name='swagger_api_docs'),
]