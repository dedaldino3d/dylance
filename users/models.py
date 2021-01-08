from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    is_premium = models.BooleanField()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


UserModel = get_user_model()


class Profile(TimeStampedModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, null=False, blank=False)
    first_name = models.CharField(verbose_name=_("first name"), max_length=80, blank=True)
    last_name = models.CharField(verbose_name=_("last name"), max_length=80, blank=True)
    picture_url = models.ImageField(blank=True, null=True, upload_to='user/profile_image/')

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
