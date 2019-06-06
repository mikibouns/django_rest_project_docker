from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from .filters import BasketFilter

from .models import Basket, ProductList
from .serializers import BasketSerializer, AddToBasketSerializer, ProductListSerializer


class BasketListViewSet(ListAPIView):
    '''
    Управление корзинами пользователей
    '''
    permission_classes = [IsAuthenticated, ]
    serializer_class = BasketSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BasketFilter

    def get_queryset(self, *args, **kwargs):
        queryset = Basket.objects.all()
        if self.request.user.is_superuser: # если суперпользователь
            return queryset # возвращаем весь список
        else: # если авторизованный пользователь: вернет корзину авторизованного пользователя
            return queryset.filter(user_id=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     '''
    #     Получить список корзин пользователей с их содержимым
    #     '''
    #     basket = self.get_queryset()
    #     serializer = self.serializer_class(basket, many=True)
    #     return Response(list(serializer.data))


class BasketDetailViewSet(GenericAPIView):
    '''
    Управление определенной корзиной
    '''
    permission_classes = [IsAuthenticated, ]
    serializer_class = AddToBasketSerializer

    def get_queryset(self):
        request_user = self.request.user
        basket = get_object_or_404(Basket, pk=self.kwargs.get('pk'))
        if basket.user_id == request_user or request_user.is_superuser:
            return basket
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        '''
        получить содержимое корзины
        '''
        basket = self.get_queryset()
        serializer = self.serializer_class(ProductList.objects.filter(basket=basket), many=True)
        return Response(list(serializer.data))

    def post(self, *args, **kwargs):
        '''
        Добавить в корзину товар
        '''
        basket = self.get_queryset()
        serializer = self.serializer_class(data=self.request.data, context={'basket': basket})
        if serializer.is_valid():
            serializer.save()
            return Response(dict(serializer.data), status=status.HTTP_201_CREATED)
        return Response({'success': 0,
                         'expection': serializer._errors,
                         'message': 400}, status=status.HTTP_400_BAD_REQUEST)


class BasketDeleteViewSet(GenericAPIView):
    '''
    Управление продуктом
    '''
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        try:
            return ProductList.objects.filter(basket__id=self.kwargs.get('pk')).get(id=self.kwargs.get('prod'))
        except ProductList.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        '''
        Получить продукт в корзине
        '''
        purchase = self.get_queryset()
        serializer = self.serializer_class(purchase)
        return Response(dict(serializer.data))

    def put(self, request, *args, **kwargs):
        '''
        измнить продукт в корзине
        '''
        purchase = self.get_queryset()
        instance = purchase
        serialiser = self.serializer_class(instance, self.request.data, partial=True)
        if serialiser.is_valid():
            serialiser.save()
            return Response(dict(serialiser.data))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        '''
        Удалить продукт из корзины
        '''
        purchase = self.get_queryset()
        ProductList.quantity_calculation(product=purchase.product,
                                         quantity=purchase.quantity * -1)
        purchase.delete()
        return Response({'success': 1, 'message': 200}, status=status.HTTP_200_OK)