from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    """Custom manager for User model with email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email-based authentication.
    Extends Django's AbstractBaseUser with additional profile fields.
    """
    
    # Contact information
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be between 9-15 digits, optionally with + prefix.',
                code='invalid_phone'
            )
        ]
    )
    
    # Personal information
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Status and security
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    
    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["-date_joined"]),
        ]

    @property
    def full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def phone_number(self) -> str:
        """Alias for phone field to match serializer."""
        return self.phone
    
    @phone_number.setter
    def phone_number(self, value: str) -> None:
        """Set phone field via phone_number property."""
        self.phone = value
    
    def __str__(self) -> str:
        return self.email