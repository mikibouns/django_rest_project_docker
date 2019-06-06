from django.http import Http404
from django.shortcuts import get_object_or_404
from .serializers import UsersSerializer, UsersUpdateSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend


from .permissions import (
    POSTOrNotForUsers
)

User = get_user_model()


class UserListViewSet(ListCreateAPIView):
    '''
    Упревление пользователями
    '''
    permission_classes = [POSTOrNotForUsers, ]
    serializer_class = UsersSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'address', 'fio')

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.user.is_superuser: # если суперпользователь
            return queryset # возвращаем весь список
        else: # если анонимный пользователь, вернет пустой список, если авторизованный: авторизованного пользователя
            return queryset.filter(id=self.request.user.id)

    # def get(self, request, *args, **kwargs):
    #     '''
    #     Получить список пользователей
    #     '''
    #     users = self.get_queryset()
    #     serializer = self.serializer_class(users, many=True)
    #     return Response(list(serializer.data))
    #
    # def post(self, request, *args, **kwargs):
    #     '''
    #     Создать пользователя
    #     '''
    #     serializer = self.serializer_class(data=self.request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         user = User.objects.get(username=serializer.data['address'])
    #         return Response({'success': 1,
    #                          'user_id': user.id,
    #                          'token': Token.objects.create(user=user).key}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'success': 0,
    #                          'expection': serializer._errors,
    #                          'message': 400}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailViewSet(GenericAPIView):
    '''
    Управление пользователем
    '''
    permission_classes = [IsAuthenticated, ]
    serializer_class = UsersUpdateSerializer

    def get_queryset(self):
        request_user = self.request.user
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        if user == request_user or request_user.is_superuser:
            return user
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        '''
        Получить детализацию по пользователю
        '''
        user = self.get_queryset()
        serializer = self.serializer_class(user)
        return Response(dict(serializer.data))

    def put(self, request, *args, **kwargs):
        '''
        Изменить пользователя
        '''
        instance = self.get_queryset()
        serializer = self.serializer_class(instance, data=self.request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(dict(serializer.data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        '''
        Удалить пользователя
        '''
        user = self.get_queryset()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
