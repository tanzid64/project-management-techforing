from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from project_management.managers import UserManager


# Create your models here.
class TimeStampMixin(models.Model):
    """
    An abstract base class model that provides self-updating 'created_at' and 'updated_at' fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """
    Custom User model with email as the unique identifier.
    """

    email = models.EmailField(
        verbose_name=_("Email Address"), unique=True, db_index=True
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # Avoid conflicts with default auth.User
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        verbose_name=_("groups"),
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # Avoid conflicts with default auth.User
        blank=True,
        help_text=_("Specific permissions for this user."),
        verbose_name=_("user permissions"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]  # Descending order

    @property
    def get_full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()


class Project(TimeStampMixin):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    description = models.TextField(verbose_name=_("Description"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-created_at"]


class ProjectMembers(models.Model):
    class RoleChoices(models.TextChoices):
        OWNER = "admin", _("Admin")
        MEMBER = "member", _("Member")

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="member_of_projects"
    )
    role = models.CharField(
        verbose_name=_("Role"), max_length=10, choices=RoleChoices.choices
    )

    class Meta:
        unique_together = ("project", "user")
        verbose_name = _("Project Member")
        verbose_name_plural = _("Project Members")

    def __str__(self):
        return f"{self.user.username}-{self.project.name}"
