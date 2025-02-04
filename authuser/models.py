from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Manager for CustomUser model with phone number login"""
    
    def create_user(self, phone, password=None, **extra_fields):
        """Create and return a regular user with phone number"""
        if not phone:
            raise ValueError("The Phone Number field is required")
        # Automatically assign a unique pass_key if not provided
        extra_fields.setdefault('pass_key', str(uuid.uuid4()))  # Generate a unique UUID for pass_key
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """Create and return a superuser with phone number"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Automatically assign a unique pass_key if not provided
        extra_fields.setdefault('pass_key', str(uuid.uuid4()))  # Generate a unique UUID for pass_key

        return self.create_user(phone, password, **extra_fields)



# Role Model
class Role(models.Model):
    ROLE_CHOICES = [
        ("gm", "General Manager"),
        ("pa", "Personal Assistant"),
        ("op", "Operator"),
    ]
    name = models.CharField(max_length=2, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()  # Returns human-readable name


# Custom User Model
class CustomUser(AbstractUser):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pass_key = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15, unique=True, verbose_name=_("Phone Number"))
    
    roles = models.ManyToManyField(Role, related_name="users")
    gm = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members',
        limit_choices_to={'roles__name': 'gm'}  # Correct lookup for gm role
    )

    USERNAME_FIELD = 'phone'  # Use phone as the unique identifier
    username = None  # Disable default username field
    REQUIRED_FIELDS = []  # Remove username from required fields

    # Custom manager
    objects = CustomUserManager()

    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.roles.filter(name=role_name).exists()

    def get_roles(self):
        """Return a list of role names"""
        return list(self.roles.values_list('name', flat=True))
