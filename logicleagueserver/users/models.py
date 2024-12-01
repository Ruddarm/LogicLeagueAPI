from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError



class UserManager(BaseUserManager):
    def create_user(self, userobj):
        # Ensure that userobj is a dictionary and the necessary fields exist
        username = userobj.get('username')
        email = userobj.get('email')
        password = userobj.get('password')

        # Validate email and username
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, userobj):
        # Create an admin user
        user = self.create_user(userobj)
        user.is_admin = True
        user.save(using=self._db)
        return user


class LogicLeagueUser(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # is_admin = models.BooleanField(default=False)
    
    # Add additional fields as needed, e.g., first_name, last_name, etc.
    
    # Set the custom manager
    objects = UserManager()

    # Define USERNAME_FIELD and REQUIRED_FIELDS
    USERNAME_FIELD = 'email'  # This is typically the unique identifier (email or username)
    REQUIRED_FIELDS = ['username']  # Fields that are required when creating a user

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Override to allow for permission checks
        return self.is_admin

    def has_module_perms(self, app_label):
        # Override to allow for module permission checks
        return self.is_admin


#user Education models 