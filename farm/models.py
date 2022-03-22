from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Farmer

from .validators import validate_possible_ph_value

FARM_AREA_UNITS = [("acre", _("acre")), ("ha", _("hectare"))]


class Farm(models.Model):
    id = models.BigAutoField(
        db_column="Farm_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField("Farm Name", max_length=256, db_column="Farm_name")
    location = models.CharField(
        "Farm Location", max_length=256, db_column="Farm_location"
    )
    area = models.PositiveBigIntegerField("Area covered", db_column="Farm_area")
    area_unit = models.CharField(
        "Farm area unit measurement",
        max_length=10,
        db_column="Farm_area_unit",
        default="acre",
        choices=FARM_AREA_UNITS,
    )
    farmer_id = models.ForeignKey(
        Farmer, on_delete=models.CASCADE, db_column="Farm_Farmer_id"
    )

    class Meta:
        db_table = "Farm"

    def __str__(self) -> str:
        return "%s - %s" % (self.name, self.location)


SOIL_COLOUR = (
    ("black", _("black")),
    ("brown", _("brown")),
    ("red", _("red")),
    ("gray", _("gray")),
    ("white", _("white")),
)

SOIL_TEXTURE = (
    ("sandy", _("sandy")),
    ("silt", _("silt")),
    ("loam", _("clay")),
    ("sandy loam", _("sandy loam")),
    ("loamy sand", _("loamy sand")),
    ("silty loam", _("silty loam")),
    ("sandy clay", _("sandy clay")),
    ("silty clay", _("silty clay")),
)


SOIL_STRUCTURE = (
    ("granular", "granular"),
    ("blocky/sub-granular", "blocky/sub-granular"),
    ("prismatic & columnar", "prismatic & columnar"),
    ("platy", "platy"),
)


class Soil(models.Model):
    id = models.BigAutoField(
        db_column="Soil_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    pH = models.DecimalField(
        "Soil pH",
        db_column="Soil_pH",
        validators=[validate_possible_ph_value],
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    pH = models.PositiveSmallIntegerField(
        "Soil pH", db_column="Soil_pH", validators=[validate_possible_ph_value]
    )  # validators
    color = models.CharField(
        "Soil color", max_length=64, choices=SOIL_COLOUR, db_column="Soil_color"
    )
    texture = models.CharField(
        "Soil texture", max_length=64, choices=SOIL_TEXTURE, db_column="Soil_texture"
    )
    structure = models.CharField(
        "Soil structure",
        max_length=256,
        choices=SOIL_STRUCTURE,
        db_column="Soil_structure",
    )
    depth = models.DecimalField(
        "Soil depth",
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        db_column="Soil_depth",
    )
    testing_date = models.DateField(
        "Soil current testing date", db_column="Soil_testing_date"
    )
    last_testing_date = models.DateField(
        "Soil last testing date", db_column="Soil_last_testing_date"
    )
    next_testing_date = models.DateField(
        "Soil next testing date", db_column="Soil_next_testing_date"
    )
    status = models.CharField(
        "Soil status", max_length=64, db_column="Soil_status"
    )  # find soil status that describe the soil
    notes = models.TextField("Soil Notes", db_column="Soil_notes", editable=True)
    farm_id = models.ForeignKey(
        Farm, on_delete=models.CASCADE, db_column="Soil_Farm_id"
    )

    class Meta:
        db_table = "Soil"

    def __str__(self):
        return "Soil test on %s" % (self.farm_id)
