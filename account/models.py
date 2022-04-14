from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .validators import validate_possible_number


class LoginManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")

        user = self.model(username=username, rank="worker", **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username=username, password=password, **extra_fields)

        user.rank = "farmer"

        user.save(using=self._db)


RANK = (
    ("farmer", "farmer"),
    ("manager", "manager"),
    ("worker", "worker"),
)


class Login(AbstractBaseUser):
    id = models.BigAutoField(
        db_column="Login_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name=_("ID"),
    )
    username = models.CharField(db_column="Login_username", max_length=32, unique=True)
    password = models.CharField(
        _("password"),
        max_length=128,
        db_column="Login_password",
    )
    rank = models.CharField(
        db_column="Login_rank", choices=RANK, default="worker", max_length=10
    )
    last_login = models.DateTimeField(
        _("last login"), db_column="Login_last_login", blank=True, null=True
    )
    is_active = models.BooleanField(
        "Account active", db_column="Login_is_active", default=True
    )
    is_staff = models.BooleanField("Is staff", db_column="Login_is_staff", default=True)

    USERNAME_FIELD = "username"

    # REQUIRED_FIELDS = ['username',]

    objects = LoginManager()

    class Meta:
        db_table = "Login"
        ordering = ("username",)

    def __str_(self):
        return f"{self.username} {self.rank}"

    def has_perm(self, perm, obj=None):
        return self.rank == "farmer" or self.rank == "manager"

    def has_module_perms(self, app_label):
        # doest the user have permissions to view the app `app_label`
        return True


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class Farmer(models.Model):
    id = models.BigAutoField(
        db_column="Farmer_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    first_name = models.CharField(
        "farmer first name", max_length=127, db_column="Farmer_first_name", blank=False
    )
    last_name = models.CharField(
        "Farmer last name", max_length=127, db_column="Farmer_last_name"
    )
    national_id = models.CharField(
        "Farmer National Identification Number",
        max_length=32,
        db_column="Farmer_national_id",
    )
    phone_no = PossiblePhoneNumberField(
        "Farmer Phone no", blank=True, default="", db_column="Farmer_phone_no"
    )
    login_id = models.ForeignKey(
        "Login",
        verbose_name="Farmer login id",
        on_delete=models.CASCADE,
        db_column="Farmer_Login_id",
    )
    # farm_id = models.ManyToManyField(Farm, verbose_name='Farm(s) owned', related_name='farms', db_column='Farmer_Farm_id')

    class Meta:
        db_table = "Farmer"
        ordering = ("first_name",)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Worker(models.Model):
    id = models.BigAutoField(
        db_column="Worker_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    first_name = models.CharField(
        "Worker first name", max_length=127, db_column="Worker_first_name"
    )
    last_name = models.CharField(
        "Worker last name", max_length=127, db_column="Worker_last_name"
    )
    national_id = models.CharField(
        "Worker National Identification Number",
        max_length=32,
        db_column="Worker_national_id",
    )
    phone_no = PossiblePhoneNumberField(
        "Worker Phone no",blank=True, default="", db_column="Worker_phone_no"
    )
    login_id = models.ForeignKey(
        "Login",
        verbose_name="Worker login id",
        on_delete=models.CASCADE,
        db_column="Worker_Login_id",
    )

    class Meta:
        db_table = "Worker"
        ordering = ("first_name",)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name
