# Generated by Django 3.2.4 on 2022-04-27 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farming", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crop",
            name="duration_measurement",
            field=models.CharField(
                choices=[
                    ("days", "days"),
                    ("week(s)", "week(s)"),
                    ("month(s)", "month(s)"),
                    ("year(s)", "year(s)"),
                ],
                db_column="Crop_duration_measurement",
                default="week(s)",
                max_length=16,
                verbose_name="Crop maturity duration measurement",
            ),
        ),
    ]
