# Generated by Django 3.2.4 on 2022-04-06 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0003_auto_20220325_2132"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farmtask",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "pending"),
                    ("ongoing", "ongoing"),
                    ("complete", "complete"),
                    ("cancelled", "cancelled"),
                ],
                db_column="Farm_Task_status",
                default="pending",
                max_length=64,
                verbose_name="Farm Task status",
            ),
        ),
    ]
