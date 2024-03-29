from django.db import models

from farm.models import Farm

DURATION = (
    ("days", "days"),
    ("week(s)", "week(s)"),
    ("month(s)", "month(s)"),
    ("year(s)", "year(s)"),
)


class Crop(models.Model):
    id = models.BigAutoField(
        db_column="Crop_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        "Crop name", max_length=127, blank=False, null=False, db_column="Crop_name"
    )
    desc = models.TextField(
        "Crop description", blank=True, null=True, db_column="Crop_desc"
    )
    variety = models.CharField(
        "Crop Variety", blank=True, null=True, max_length=127, db_column="Crop_variety"
    )
    maturity_duration = models.PositiveIntegerField(
        "Crop maturity duration", db_column="Crop_maturity_duration"
    )
    duration_measurement = models.CharField(
        "Crop maturity duration measurement",
        max_length=16,
        default="week(s)",
        choices=DURATION,
        db_column="Crop_duration_measurement",
    )

    class Meta:
        db_table = "Crop"

    def __str__(self):
        return "%s - %s" % (self.name, self.variety)


class FarmingStage(models.Model):
    id = models.BigAutoField(
        db_column="Farming_stage_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        "Farming Stage name", max_length=64, db_column="Farming_stage_name"
    )
    desc = models.TextField(
        "Farming Stage description", db_column="Farming_stage_desc", blank=True
    )

    class Meta:
        db_table = "Farming_stage"

    def __str__(self):
        return "%s" % self.name


YIELDS_MEASUREMENT = (
    ("KGS", "kgs"),
    ("TONS", "tons"),
    ("BAGS", "bags"),
)


class FarmingSeason(models.Model):
    id = models.BigAutoField(
        db_column="Farming_season_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        "Farming season name", max_length=64, db_column="Farming_season_name"
    )
    desc = models.TextField(
        "Farming season description", blank=True, db_column="Farming_season_desc"
    )
    start_date = models.DateField(
        "Farming season start date",
        blank=False,
        null=False,
        db_column="Farming_season_start_date",
    )
    end_date = models.DateField(
        "Farming season end date",
        blank=False,
        null=False,
        db_column="Farming_season_end_date",
    )
    farm = models.ForeignKey(
        Farm,
        verbose_name="Farm",
        on_delete=models.CASCADE,
        db_column="Farming_season_Farm_id",
    )
    crop = models.ForeignKey(
        Crop,
        verbose_name="Crop planted",
        related_name="crops",
        on_delete=models.CASCADE,
        db_column="Farming_season_Crop_id",
    )
    stage = models.ForeignKey(
        FarmingStage,
        related_name="stages",
        null=True,
        on_delete=models.SET_NULL,
        db_column="Farming_season_current_Farming_stage_id",
    )
    yields = models.PositiveIntegerField(
        "Season's yields", default=0, db_column="Farming_season_yields", blank=True
    )
    yields_measurement = models.CharField(
        "Yields measurement",
        choices=YIELDS_MEASUREMENT,
        max_length=32,
        blank=True,
        default="KGS",
        db_column="Farming_season_yields_measurement",
    )

    class Meta:
        db_table = "Farming_season"

    def __str__(self):
        return "%s" % self.name
