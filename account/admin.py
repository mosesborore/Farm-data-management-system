from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.forms import LoginForm

from .models import Farmer, Login, Worker

admin.site.site_header = "Farm Data Management Administration"
admin.site.login_form = LoginForm
admin.site.index_title = "Administration Site"
admin.site.site_title = "Farm Data Management Admin Site"

# UserCreationForm === refer Customizing authentication in Django¶ documentation
# UserChangeForm


# Register your models here.
class LoginAdmin(UserAdmin):
    """admin options  and functionalities"""

    list_display = ("username", "rank")
    search_fields = ("username",)
    readonly_fields = ("id",)

    filter_horizontal = ()
    list_filter = ()

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("rank",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "rank"),
            },
        ),
    )


class FarmerAdmin(ModelAdmin):
    list_display = ("first_name", "last_name", "national_id", "phone_no")
    search_fields = (
        "first_name",
        "last_name",
        "national_id",
        "phone_no",
    )
    readonly_fields = ("id",)


class WorkerAdmin(ModelAdmin):
    list_display = ("first_name", "last_name", "national_id", "phone_no", "login_id")
    search_fields = (
        "first_name",
        "last_name",
        "national_id",
        "phone_no",
    )
    readonly_fields = ("id",)

    list_select_related = True


admin.site.register(Login, LoginAdmin)
# since we're not using Django's built-in permissions
# we unregister the Group model from admin
admin.site.unregister(Group)

admin.site.register(Farmer, FarmerAdmin)

admin.site.register(Worker, WorkerAdmin)
