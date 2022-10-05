from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import UserSerializer, FollowSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    # permission_classes = (
    #     GetPostOnly,
    #     IsAuthenticated,
    # )
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('^following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)