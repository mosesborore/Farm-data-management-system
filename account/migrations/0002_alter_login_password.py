# Generated by Django 3.2.4 on 2022-03-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="login",
            name="password",
            field=models.CharField(
                db_column="Login_password", max_length=128, verbose_name="password"
            ),
        ),
    ]
