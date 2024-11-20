from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse



class CustomUserManagaer(BaseUserManager):
    def create_user(self,user_name,user_email,password=None):
        if not user_email:
            raise ValueError(_('Email cannot be empty'))
        user_email=self.normalize_email(user_email);
        user = self.model(user_name=user_name,user_email=user_email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, user_name, user_email, password=None):
        user = self.create_user(user_name, user_email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.

class User (AbstractBaseUser):
    user_name = models.CharField(max_length=100, null=False)
    user_email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)

    objects = CustomUserManagaer()

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})
