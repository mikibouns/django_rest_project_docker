from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductsSerializer, ProductsUpdateSerializer
from .models import Products
from .permissions import (
    IsAdminOrReadOnly
)


class ProductsListViewSet(ListCreateAPIView):
    '''
    Управление продукцией
    '''
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = ProductsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = '__all__'

    def get_queryset(self):
        queryset = Products.objects.all()
        if self.request.user.is_superuser: # если суперпользователь
            return queryset # возвращаем весь список
        else: # если пользователь не администратор показать товар который есть в наличии
            return queryset.exclude(quantity=0).order_by('art')

    # def get(self, request, *args, **kwargs):
    #     '''
    #     Получить список продукции
    #     '''
    #     products = self.get_queryset()
    #     serializer = self.serializer_class(products, many=True)
    #     return Response(list(serializer.data))

    # def post(self, request, *args, **kwargs):
    #     '''
    #     Добавить продукцию
    #     '''
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(dict(serializer.data), status=status.HTTP_201_CREATED)
    #     return Response({'success': 0,
    #                      'expection': serializer._errors,
    #                      'message': 400}, status=status.HTTP_400_BAD_REQUEST)


class ProductsDetailViewSet(GenericAPIView):
    '''
    Управление определенным продуктом
    '''
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductsUpdateSerializer

    def get_queryset(self):
        return get_object_or_404(Products, art=self.kwargs.get('art'))

    def get(self, request, *args, **kwargs):
        '''
        Получить продукт
        '''
        product = self.get_queryset()
        serializer = self.serializer_class(product)
        return Response(dict(serializer.data))

    def put(self, request, *args, **kwargs):
        '''
        Изменить продукт
        '''
        product = Products.objects.get(art=kwargs.get('art'))
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(dict(serializer.data), status=status.HTTP_201_CREATED)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        '''
        Удалить продукт
        '''
        user = self.get_queryset()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




