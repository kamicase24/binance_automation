"""User View"""

from binance_automation.base import serializers
import logging
from rest_framework import mixins
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from binance_automation.users.permissions.user import isAdmin

log = logging.getLogger(__name__)

from binance_automation.users.models.user import User
from binance_automation.users.serializers.user import (
    PasswordRecoverySerializer,
    PasswordUpdateSerializer,
    UserModelSerializer, 
    LoginSerializer, 
    RegisterModelSerializer)


class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    fields = ('first_name', 'last_name', 'username', 'email', 'is_active')
    filterset_fields = fields
    search_fields = fields

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ['logout']:
            permissions = [IsAuthenticated] 
        return [p() for p in permissions]

    @swagger_auto_schema(request_body=RegisterModelSerializer)
    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        """
        Register new User
        """
        serializer = RegisterModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=LoginSerializer)
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """
        Login user
        """
        serializer = LoginSerializer(data=request.data)
        serializer.context.update(request=request)
        serializer.is_valid(raise_exception=False)
        if serializer.errors:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        """
        Logout user
        """
        request.user.auth_token.delete()
        return Response({}, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=PasswordRecoverySerializer)
    @action(detail=False, methods=['post'])
    def password_recovery(self, request, *args, **kwargs):
        serializer = PasswordRecoverySerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        if serializer.errors:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        email = serializer.save()
        data = {'success': f'Correo enviado a {email}'}
        return Response(data, status.HTTP_200_OK)


    @swagger_auto_schema(request_body=PasswordUpdateSerializer)
    @action(detail=False, methods=['post'])
    def password_update(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status.HTTP_200_OK)
