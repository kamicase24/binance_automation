"""User Serializer"""
from datetime import timedelta
import logging

from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.db.models import fields

from rest_framework import serializers

from binance_automation.utils.send_mail import SendMail
from binance_automation.users.models.user import User

log = logging.getLogger(__name__)


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'username',
            'token'
        )

class RegisterModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    permission = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'token',
            'permission',
        )

    def validate(self, data):
        permission = data.pop('permission', False)
        if permission:
            if permission not in ['staff', 'external']:
                raise serializers.ValidationError({
                    'code': 'US00',
                    'message': "Permiso invalido. Valores validos: 'staff', 'external'"
                })
            else:
                self.context.update({'permission': permission})

        return data

    def create(self, validated_data):

        res = User.objects.create_user(**validated_data)
        permission = self.context.get('permission', 'anonymous')
        if permission == 'staff':
            setattr(res, 'is_staff', True)
        elif permission == 'external':
            setattr(res, 'is_external', True)

        res.save()
        return res

    

class LoginSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    site_id = serializers.DictField(read_only=True)
    site_ids = serializers.ListField(read_only=True, required=False)
    user_type_id = serializers.DictField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'site_id',
            'token',
            'site_ids',
            'user_type_id'
        )

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        request = self.context.get('request')
        
        if email is None:
            raise serializers.ValidationError('Correo Electronico Requerido')

        if password is None:
            raise serializers.ValidationError('Contraseña Requerida')

        user = authenticate(username=email.lower(), password=password)

        if user is None:
            raise serializers.ValidationError(
                'Usuario o Contraseña incorrectos. No se ha conseguido ningún usuario'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Usuario desactivado.'
            )
            
        result = {
            'email': user.email,
            'username': user.username,
            'token': user.token,
            'id': user.id,
        }
        return result

class PasswordRecoverySerializer(serializers.Serializer):
    
    email = serializers.CharField(max_length=255)
    origin = serializers.CharField(max_length=255)



    def validate(self, data):
        email = data.get('email', None)
        if email is None:
            raise serializers.ValidationError('Correo Eléctronico Requerido')

        try:
            user_id = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuario no registrado, por favor comunicarse con su administrador')

        data.update(user_id=user_id)
        return data

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        email = validated_data['email'].lower()
        sm = SendMail()
        origin = validated_data.get('origin', 'http://trackmybus.com/')
        verification_token = user_id._generate_jwt_token()
        link = f'{origin}password_update/?token={verification_token}'
        
        # sm.send_email(
        #     settings.SERVER_EMAIL,
        #     email,
        #     'Recuperación de Contraseña',
        #     'password_recovery_request.html',
        #     {
        #         'link': link,
        #         'name': validated_data['op_user_id'].name
        #     }
        # )
        return email


class PasswordUpdateSerializer(serializers.Serializer):

    user_id = serializers.IntegerField()
    new_password = serializers.CharField(min_length=8, max_length=64)
    password_confirm = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user_id = data.get('user_id', None)
        new_password = data.get('new_password', None)
        password_confirm = data.get('password_confirm', None)

        if user_id is None:
            raise serializers.ValidationError('ID de Usuario Requerido')
        if new_password is None:
            raise serializers.ValidationError('Nueva Contraseña Requerida')
        if password_confirm is None:
            raise serializers.ValidationError('Confirmación de Contraseña Requerida')

        if new_password != password_confirm:
            raise serializers.ValidationError('Las Contraseñas no coinciden')

        password_validation.validate_password(new_password)

        try:
            user_id = User.objects.get(pk=user_id)
            data.update(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuario no existe')

        if user_id.check_password(new_password):
            raise serializers.ValidationError(
                'La Contraseña no puede ser la misma al a anterior'
            )
        return data


    def create(self, validated_data):
        new_password = validated_data.get('new_password')
        user_id = validated_data.get('user_id')
        user_id.set_password(new_password)
        user_id.save()
        return {
            'success': True,
            'message': 'Contraseña Actualizada'
        }
        
