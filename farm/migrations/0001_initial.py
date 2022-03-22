# Generated by Django 3.2.4 on 2022-03-19 18:06

import django.db.models.deletion
from django.db import migrations, models

import farm.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Farm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        db_column="Farm_id",
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_column="Farm_name", max_length=256, verbose_name="Farm Name"
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        db_column="Farm_location",
                        max_length=256,
                        verbose_name="Farm Location",
                    ),
                ),
                (
                    "area",
                    models.PositiveBigIntegerField(
                        db_column="Farm_area", verbose_name="Area covered"
                    ),
                ),
                (
                    "area_unit",
                    models.CharField(
                        choices=[("acre", "acre"), ("ha", "hectare")],
                        db_column="Farm_area_unit",
                        default="acre",
                        max_length=10,
                        verbose_name="Farm area unit measurement",
                    ),
                ),
                (
                    "farmer_id",
                    models.ForeignKey(
                        db_column="Farm_Farmer_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.farmer",
                    ),
                ),
            ],
            options={
                "db_table": "Farm",
            },
        ),
        migrations.CreateModel(
            name="Soil",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        db_column="Soil_id",
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pH",
                    models.PositiveSmallIntegerField(
                        db_column="Soil_pH",
                        validators=[farm.validators.validate_possible_ph_value],
                        verbose_name="Soil pH",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("black", "black"),
                            ("brown", "brown"),
                            ("red", "red"),
                            ("gray", "gray"),
                            ("white", "white"),
                        ],
                        db_column="Soil_color",
                        max_length=64,
                        verbose_name="Soil color",
                    ),
                ),
                (
                    "texture",
                    models.CharField(
                        choices=[
                            ("sandy", "sandy"),
                            ("silt", "silt"),
                            ("loam", "clay"),
                            ("sandy loam", "sandy loam"),
                            ("loamy sand", "loamy sand"),
                            ("silty loam", "silty loam"),
                            ("sandy clay", "sandy clay"),
                            ("silty clay", "silty clay"),
                        ],
                        db_column="Soil_texture",
                        max_length=64,
                        verbose_name="Soil texture",
                    ),
                ),
                (
                    "structure",
                    models.CharField(
                        choices=[
                            ("granular", "granular"),
                            ("blocky/sub-granular", "blocky/sub-granular"),
                            ("prismatic & columnar", "prismatic & columnar"),
                            ("platy", "platy"),
                        ],
                        db_column="Soil_structure",
                        max_length=256,
                        verbose_name="Soil structure",
                    ),
                ),
                (
                    "depth",
                    models.DecimalField(
                        db_column="Soil_depth",
                        decimal_places=2,
                        max_digits=12,
                        verbose_name="Soil depth",
                    ),
                ),
                (
                    "testing_date",
                    models.DateField(
                        db_column="Soil_testing_date",
                        verbose_name="Soil current testing date",
                    ),
                ),
                (
                    "last_testing_date",
                    models.DateField(
                        db_column="Soil_last_testing_date",
                        verbose_name="Soil last testing date",
                    ),
                ),
                (
                    "next_testing_date",
                    models.DateField(
                        db_column="Soil_next_testing_date",
                        verbose_name="Soil next testing date",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        db_column="Soil_status",
                        max_length=64,
                        verbose_name="Soil status",
                    ),
                ),
                (
                    "notes",
                    models.TextField(db_column="Soil_notes", verbose_name="Soil Notes"),
                ),
                (
                    "farm_id",
                    models.ForeignKey(
                        db_column="Soil_Farm_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="farm.farm",
                    ),
                ),
            ],
            options={
                "db_table": "Soil",
            },
        ),
    ]
