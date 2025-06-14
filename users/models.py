from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("The user must have an email address")
        if not username:
            raise ValueError("The user must have a username")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    reset_password_token = models.CharField(max_length=100, blank=True, null=True)  

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Fixes conflict with auth.User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Fixes conflict with auth.User
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


