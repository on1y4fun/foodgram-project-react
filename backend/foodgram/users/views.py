from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.permissions import CreateUserOrAuthenticated
from api.serializers import (
    FollowSerializer,
    UserPasswordSerializer,
    UserSerializer,
)
from users.models import Follow, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (CreateUserOrAuthenticated,)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if not request.method == 'DELETE':
            if user.follower.filter(author=author).exists():
                return Response(
                    'Вы уже подписаны', status=status.HTTP_400_BAD_REQUEST
                )
            if not user == author:
                instance = Follow.objects.create(user=user, author=author)
                serializer = UserSerializer(author)
                return Response(serializer.data)
            return Response(
                'Нельзя подписаться на самого себя',
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.follower.get(author=author).delete()
        return Response('Успешная отписка', status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def set_password(self, request):
        user = request.user
        serializer = UserPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        data = serializer.data
        if not user.check_password(data.get('current_password')):
            return Response(
                'Неправильный пароль', status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(data.get('new_password'))
        user.save()
        return Response('Пароль изменен', status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)
