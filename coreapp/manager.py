from datetime import datetime

from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('The Mobile Number must be set')
        # email = self.normalize_email(email)
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        # user.country_id = 19
        user.dob = datetime.now().date()
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_approved', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(mobile, password, **extra_fields)
