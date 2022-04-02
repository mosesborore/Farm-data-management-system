from django.conf import settings
from django.db import models as models
from django_prices.models import MoneyField
from tinymce import models as tinymce_models

from account.models import Worker
from farm.models import Farm
from farming.models import FarmingSeason
from input.models import InputProduct

FARM_TASK_STATUS = (
    (
        "pending",
        "pending",
    ),
    (
        "ongoing",
        "ongoing",
    ),
    (
        "complete",
        "complete",
    ),
    (
        "cancelled",
        "cancelled",
    ),
)


class FarmTask(models.Model):
    id = models.BigAutoField(
        db_column="Farm_Task_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        "Farm Task Name", max_length=256, db_column="Farm_Task_name"
    )
    start_date = models.DateField(
        "Farm Task start date", db_column="Farm_Task_start_date"
    )
    deadline = models.DateField("Farm Task end date", db_column="Farm_Task_deadline")
    updated_on = models.DateField(
        "Farm Task updated on", auto_now=True, db_column="Farm_Task_updated_on"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="Farm_Task_created_by",
    )
    objectives = tinymce_models.HTMLField(
        "Farm objectives", db_column="Farm_Task_objectives"
    )
    notes = tinymce_models.HTMLField(
        "Farm Task notes", db_column="Farm_Task_notes", blank=True
    )
    status = models.CharField(
        "Farm Task status",
        choices=FARM_TASK_STATUS,
        max_length=64,
        db_column="Farm_Task_status",
        default="pending",
    )
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
        blank=True,
        null=True,
    )
    expected_expenses_price_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    expected_expenses = MoneyField(
        amount_field="expected_expenses_price_amount",
        currency_field="currency",
        verbose_name="expected expenses",
        db_column="Farm_Task_expected_expenses",
    )
    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, db_column="Farm_Task_Farm_id"
    )
    products = models.ManyToManyField(
        InputProduct,
        verbose_name="Farm Task product to use",
        db_column="Farm_Task_Input_product_id",
        blank=True,
    )
    product_units_used = models.PositiveIntegerField(
        "Input product units used",
        db_column="Farm_Task_Input_product_units_used",
        default=0,
    )
    farming_season = models.ForeignKey(
        FarmingSeason,
        verbose_name="Farm Task Farming season",
        on_delete=models.CASCADE,
        db_column="Farm_Task_Farming_season_id",
    )
    workers = models.ManyToManyField(
        Worker,
        verbose_name="Workers to carry out this task",
        db_column="Farm_Task_Worker_id",
    )

    class Meta:
        db_table = "Farm_Task"
        ordering = ("-start_date",)

    def __str__(self):
        return "%s" % self.name
