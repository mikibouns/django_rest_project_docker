from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_token
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

    path('api/v1/drf_api_docs/', include_docs_urls(title='API')),
    path('api/v1/get-token/', auth_token.obtain_auth_token, name='get_token'),
    path('api/v1/', include('main_app.urls', namespace='main_app')),
    path('api/v1/users/', include('auth_app.urls', namespace='auth')),
    path('api/v1/products/', include('product_app.urls', namespace='product')),
    path('api/v1/basket/', include('basket_app.urls', namespace='basket')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)