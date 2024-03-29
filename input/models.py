from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models import F
from django.forms import SlugField
from django.utils.translation import gettext_lazy as _
from django_prices.utils.formatting import format_price


class InputCategory(models.Model):
    id = models.BigAutoField(
        db_column="Input_category_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        "Input Category name", max_length=256, db_column="Input_category_name"
    )
    desc = models.TextField(
        "Input Category description", db_column="Input_category_desc", blank=True
    )

    class Meta:
        db_table = "Input_category"
        verbose_name_plural = "Input Categories"

    def __str__(self):
        return self.name


# unit_measurement column choices
UNIT_MEASUREMENT = (
    ("KG", _("kilograms")),
    ("G", _("grams")),
    ("L", _("liter")),
    ("BAG", _("bag")),
)

# unit_rate_measurement column choices
UNIT_RATE_MEASUREMENT = (
    ("KG/acre", _("kilogram/acre")),
    ("L/acre", _("liter/acre")),
    ("G/acre", _("grams/acre")),
    ("KG/ha", _("kilogram/hectare")),
    ("L/ha", _("liter/hectare")),
    ("G/hectare", _("grams/hectare")),
    ("bag/acre", _("bags/acre")),
    ("bag/hectare", _("bags/hectare")),
)


class InputProduct(models.Model):
    id = models.BigAutoField(
        db_column="Input_product_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        "Product name", max_length=256, db_column="Input_product_name"
    )
    desc = models.TextField(
        "Input product description", db_column="Input_product_desc", blank=True
    )
    unit_price = models.DecimalField(
        "Price per unit",
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        db_column="Input_product_unit_price",
    )
    total_units = models.PositiveBigIntegerField(
        "Product total units", db_column="Input_product_total_units", default=0
    )
    total_cost = models.DecimalField(
        "Total Amount",
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0.0,
        db_column="Input_product_total_cost",
    )
    unit_weight = models.PositiveIntegerField(
        "Product unit weight", db_column="Input_product_unit_weight"
    )
    unit_measurement = models.CharField(
        "Product unit measurement",
        max_length=5,
        choices=UNIT_MEASUREMENT,
        db_column="Input_product_unit_measurement",
        default="KG",
    )
    unit_rate = models.PositiveIntegerField(
        "Product unit rate (rate at which it is used)",
        db_column="Input_product_unit_rate",
    )
    unit_rate_measurement = models.CharField(
        "Product unit rate measurement",
        max_length=32,
        choices=UNIT_RATE_MEASUREMENT,
        db_column="Input_product_unit_rate_measurement",
        default="KG/acre",
    )
    category = models.ForeignKey(
        InputCategory,
        on_delete=models.CASCADE,
        db_column="Input_product_Input_category_id",
    )

    available_units = models.PositiveBigIntegerField(
        "Available Units",
        default=0,
        blank=True,
        db_column="Input_product_available_quantity",
    )

    class Meta:
        db_table = "Input_product"

    def calculate_total_cost(self):
        cost = self.unit_price * self.total_units
        return cost

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        return super().save(*args, **kwargs)

    def increase_unit(self, quantity: int, commit: bool = True):
        """increase the available unit of product"""
        self.available_units = F("available_units") + quantity
        self.total_units = F("total_units") + quantity
        self.total_cost = self.calculate_total_cost()
        if commit:
            self.save(
                update_fields=["total_net_amount", "total_units", "available_units"]
            )

    def decrease_unit(self, quantity: int, commit: bool = True):
        """decrease the available unit of product"""
        self.available_units = F("available_units") - quantity
        if commit:
            self.save(update_fields=["available_units"])

    def get_unit_price(self):
        """get formatted unit_price"""
        return format_price(self.unit_price, "KSH")

    def get_total_cost(self):
        """get formatted total_cost"""
        return format_price(self.total_cost, "KSH")

    def __str__(self):
        status = "available" if self.available_units else "not available"
        return "%s - %d - %s" % (self.name, self.unit_price, status)


class InputInventory(models.Model):
    id = models.BigAutoField(
        db_column="Input_Inventory_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        "Input Inventory name", max_length=127, db_column="Input_Inventory_name"
    )
    slug = SlugField(allow_unicode=True)
    desc = models.TextField(
        "Input Inventory description", db_column="Input_Inventory_desc", blank=True
    )
    ref_code = models.CharField(
        "Input Inventory reference code",
        unique=True,
        blank=True,
        max_length=36,
        db_column="Input_Inventory_ref_code",
    )
    created_on = models.DateTimeField(
        "Input Inventory created on",
        auto_now_add=True,
        db_column="Input_Inventory_created_on",
    )
    updated_on = models.DateTimeField(
        "Input Inventory updated on",
        auto_now=True,
        db_column="Input_Inventory_updated_on",
    )

    class Meta:
        db_table = "Input_Inventory"
        verbose_name_plural = "Input Inventories"

    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = str(uuid4()).rsplit("-")[-1]
        return super().save(*args, **kwargs)

    def get_total_cost(self):
        """returns the total cost for this inventory"""
        total_cost = sum([item.total_cost for item in self.items.all()])
        return format_price(total_cost, "KSH", html=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.ref_code)


class InputInventoryItem(models.Model):
    id = models.BigAutoField(
        db_column="Input_Inventory_item_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    input_product = models.ForeignKey(
        InputProduct,
        related_name="products",
        on_delete=models.CASCADE,
        db_column="Input_Inventory_item_Input_product_id",
    )
    quantity = models.PositiveIntegerField(
        "Input Inventory item quantity", db_column="Input_Inventory_item_quantity"
    )
    total_cost = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0.0,
        db_column="Input_Inventory_item_total_cost",
    )
    input_inventory = models.ForeignKey(
        InputInventory,
        on_delete=models.CASCADE,
        related_name="items",
        db_column="Input_Inventory_item_Input_Inventory_id",
    )

    class Meta:
        db_table = "Input_Inventory_item"

    def get_total(self):
        pass

    def get_total_cost(self):
        return format_price(self.total_cost, "KSH")

    def __str__(self):
        return "%s - %s Inventory Item" % (
            self.input_product.name,
            self.input_inventory.name,
        )
