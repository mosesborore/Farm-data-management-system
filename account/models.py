from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

from .validators import validate_possible_number


class LoginManager(BaseUserManager):
    def create_user(
        self, username, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            username=username, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username=username, password=password, **extra_fields)

        user.is_admin = True
        user.is_manager = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)


class Login(PermissionsMixin, AbstractBaseUser):
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
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="late joined", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    avatar = VersatileImageField(
        upload_to="user-profile-images",
        height_field="height",
        width_field="width",
        blank=True,
        null=True,
        verbose_name="Profile picture",
        default="defaultprofile.png",
    )
    height = models.PositiveIntegerField("Profile Image Height", blank=True, null=True)
    width = models.PositiveIntegerField("Profile Image Width", blank=True, null=True)

    USERNAME_FIELD = "username"

    # REQUIRED_FIELDS = ['username',]

    objects = LoginManager()

    class Meta:
        db_table = "Login"
        ordering = ("username",)

    def __str_(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_manager

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
        blank=True, default="", db_column="Farmer_phone_no"
    )
    login_id = models.ForeignKey(
        "Login",
        verbose_name="login id",
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
        blank=True, default="", db_column="Worker_phone_no"
    )
    login_id = models.ForeignKey(
        "Login",
        verbose_name="login id",
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


# Login Model Signal
@receiver(models.signals.post_save, sender=Login)
def warm_Account_profile_images(sender, instance, **kwargs):
    profile_img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set="user_avatars",
        image_attr="avatar",
    )

    num_created, failed_to_create = profile_img_warmer.warm()
    if num_created:
        print("successful image warmer created")
    if failed_to_create:
        print("unsuccessful image warmer")
