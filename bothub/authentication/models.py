from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator, _lazy_re_compile
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.dispatch import receiver


user_nickname_re = _lazy_re_compile(r"^[-a-zA-Z0-9_]+\Z")
validate_user_nickname_format = RegexValidator(
    user_nickname_re,
    _(
        "Enter a valid 'nickname' consisting of letters, numbers, "
        + "underscores or hyphens."
    ),
    "invalid",
)


def validate_user_nickname_value(value):
    if value in [
        "api",
        "docs",
        "admin",
        "ping",
        "static",
        settings.BOTHUB_BOT_NICKNAME,
    ]:
        raise ValidationError(_("The user nickname can't be '{}'").format(value))


class UserManager(BaseUserManager):
    def _create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not nickname:
            raise ValueError("The given nick must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, nickname, password, **extra_fields)

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, nickname, password, **extra_fields)


class RepositoryOwner(models.Model):
    class Meta:
        verbose_name = _("repository organization")

    REQUIRED_FIELDS = ["nickname"]

    name = models.CharField(_("name"), max_length=32, help_text=_("User's name."))
    locale = models.CharField(
        _("locale"), max_length=48, help_text=_("User's locale."), blank=True
    )
    nickname = models.CharField(
        _("nickname"),
        max_length=150,
        validators=[validate_user_nickname_format, validate_user_nickname_value],
        help_text=_(
            "User's or Organization nickname, using letters, numbers, underscores "
            + "and hyphens without spaces."
        ),
        unique=True,
    )
    biography = models.TextField(_("biography"), blank=True, null=True)
    joined_at = models.DateField(_("joined at"), auto_now_add=True)

    def __str__(self):
        return self.name  # pragma: no cover

    @property
    def is_anonymous(self):
        return False if self.is_organization else self.user.is_anonymous

    @property
    def user(self):
        return getattr(self, "user_owner", None)

    @property
    def organization(self):
        return getattr(self, "organization_owner", None)

    @property
    def is_organization(self):
        return True if self.organization else False

    @property
    def repository_owner(self):
        return self


class User(AbstractBaseUser, RepositoryOwner, PermissionsMixin):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    USERNAME_FIELD = "email"

    email = models.EmailField(_("email"), unique=True, help_text=_("User's email."))

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    repository_owner = models.OneToOneField(
        RepositoryOwner,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name="user_owner",
    )

    objects = UserManager()

    @property
    def token_generator(self):
        return PasswordResetTokenGenerator()

    def send_welcome_email(self):
        if not settings.SEND_EMAILS:
            return False  # pragma: no cover
        context = {"name": self.name, "base_url": settings.BASE_URL}
        send_mail(
            _("Welcome to Bothub"),
            render_to_string("authentication/emails/welcome.txt", context),
            None,
            [self.email],
            html_message=render_to_string(
                "authentication/emails/welcome.html", context
            ),
        )

    def make_password_reset_token(self):
        return self.token_generator.make_token(self)

    def send_reset_password_email(self):
        if not settings.SEND_EMAILS:
            return False  # pragma: no cover
        token = self.make_password_reset_token()
        reset_url = "{}reset-password/{}/{}/".format(
            settings.BOTHUB_WEBAPP_BASE_URL, self.nickname, token
        )
        context = {"reset_url": reset_url, "base_url": settings.BASE_URL}
        send_mail(
            _("Reset your bothub password"),
            render_to_string("authentication/emails/reset_password.txt", context),
            None,
            [self.email],
            html_message=render_to_string(
                "authentication/emails/reset_password.html", context
            ),
        )

    def check_password_reset_token(self, token):
        return self.token_generator.check_token(self, token)

    @staticmethod
    def generate_repository_user_bot():
        user, create = User.objects.get_or_create(
            email=settings.BOTHUB_BOT_EMAIL,
            name=settings.BOTHUB_BOT_NAME,
            nickname=settings.BOTHUB_BOT_NICKNAME,
            locale="",
            is_staff=False,
            is_active=False,
        )
        return user


@receiver(models.signals.post_save, sender=User)
def send_welcome_email(instance, created, **kwargs):
    if created:
        instance.send_welcome_email()
