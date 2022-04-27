# Generated by Django 3.2.4 on 2022-04-23 13:45

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farmer",
            name="login_id",
            field=models.ForeignKey(
                db_column="Farmer_Login_id",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Farmer login id",
            ),
        ),
        migrations.AlterField(
            model_name="farmer",
            name="phone_no",
            field=account.models.PossiblePhoneNumberField(
                blank=True,
                db_column="Farmer_phone_no",
                default="",
                max_length=128,
                region=None,
                verbose_name="Farmer Phone no",
            ),
        ),
        migrations.AlterField(
            model_name="worker",
            name="login_id",
            field=models.ForeignKey(
                db_column="Worker_Login_id",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Worker login id",
            ),
        ),
        migrations.AlterField(
            model_name="worker",
            name="phone_no",
            field=account.models.PossiblePhoneNumberField(
                blank=True,
                db_column="Worker_phone_no",
                default="",
                max_length=128,
                region=None,
                verbose_name="Worker Phone no",
            ),
        ),
    ]
