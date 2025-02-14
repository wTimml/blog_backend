import uuid
import os
from django.core.files.storage import default_storage
import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not specified a valid e-mail address")
    
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True, default="Unnamed User")
    avatar = models.ImageField(upload_to='uploads/avatars', null=True, blank=True, default='uploads/avatars/default.jpg')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    on_delete=models.CASCADE

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def validate_avatar(self, file):
        MAX_SIZE = 5 * 1024 * 1024
        VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
        
        if file.size > MAX_SIZE:
            raise ValueError("File size cannot exceed 5MB")
        
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in VALID_EXTENSIONS:
            raise ValueError("Invalid file type")
        
        return ext

    def update_avatar(self, avatar_file):
        try:
            # Validate new image
            file_ext = self.validate_avatar(avatar_file)
            
            # Delete old avatar if it exists
            if self.avatar:
                try:
                    old_path = self.avatar.path
                    default_storage.delete(old_path)
                except Exception as e:
                    logger.error(f"Error deleting old avatar for user {self.id}: {e}")
            
            # Save new avatar
            new_filename = f'avatars/{self.pk}{file_ext}'
            self.avatar = default_storage.save(new_filename, avatar_file)
            self.save()
            
        except Exception as e:
            raise ValueError(f"Error updating avatar: {str(e)}")

    def update_name(self, new_name):
        if not new_name or len(new_name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self.name = new_name.strip()
        self.save()

    def update_is_staff(self, new_status):
        if not new_status or len(new_status.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self.is_staff = new_status.strip()
        self.save()

    def avatar_url(self):
        if self.avatar:
            return f'{settings.WEBSITE_URL}{self.avatar.url}'
        else:
            return ''