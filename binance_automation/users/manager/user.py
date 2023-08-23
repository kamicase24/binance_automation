from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, first_name='new_user_first_name', last_name='new_user_last_name'):
        if username is None:
            raise TypeError('Usuario requerido')

        if email is None:
            raise TypeError('Correo Electronico requerido')

        user = self.model(
            username=username, 
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, first_name, last_name):
        """
        Create and return a user object with superuser permissions (an Admin user)
        """

        if password is None:
            raise TypeError('Contraseña requerida')

        user = self.create_user(username, email, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user