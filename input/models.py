from enum import unique
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.forms import SlugField
from django.utils.translation import gettext_lazy as _
from django_prices.models import MoneyField


class InputCategory(models.Model):
    id = models.BigAutoField(db_column='Input_category_id',auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField('Input Category name', max_length=256, db_column='Input_category_name')
    desc = models.TextField("Input Category description", db_column='Input_category_desc')
    
    class Meta:
        db_table ='Input_category'
    
    def __str__(self):
        return self.name


# unit_measurement column choices      
UNIT_MEASUREMENT = (
    ('KG', _('kilograms')),
    ('G', _('grams')),
    ('L', _('liter')),
    ('BAG', _('bag')),
)

# unit_rate_measurement column choices      
UNIT_RATE_MEASUREMENT = (
    ("KG/acre", _('kilogram/acre')),
    ('L/acre', _("liter/acre")),
    ('G/acre', _('grams/acre')),
    ("KG/ha", _('kilogram/hectare')),
    ('L/ha', _("liter/hectare")),
    ('G/hectare', _('grams/hectare')),
)


class InputProduct(models.Model):
    id = models.BigAutoField(db_column='Input_product_id',auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField('Product name', max_length=256, db_column='Input_product_name')
    desc = models.TextField("Input product description", db_column='Input_product_desc')
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
        blank=True,
        null=True,
    )
    unit_price_amount = models.DecimalField(
        "Price per unit",
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        
    )
    unit_price = MoneyField(amount_field="unit_price_amount", currency_field="currency", db_column='Input_product_unit_price')
    total_units = models.PositiveBigIntegerField('Product total units', db_column='Input_product_total_cost')
    total_net_amount = models.DecimalField(
        "Total Amount",
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0.0,
    )
    total_cost = MoneyField(amount_field="total_net_amount", currency_field="currency")
    unit_weight = models.PositiveIntegerField('Product unit weight', db_column='Input_product_unit_weight')
    unit_measurement = models.CharField(
        'Product unit measurement', max_length=5, choices=UNIT_MEASUREMENT, 
        db_column='Input_product_unit_measurement', default="KG"
    )
    unit_rate = models.PositiveIntegerField('Product unit rate (rate at which it is used)', db_column='Input_product_unit_rate')
    unit_rate_measurement = models.CharField(
        'Product unit rate measurement', max_length=32, choices=UNIT_RATE_MEASUREMENT,
        db_column='Input_product_unit_rate_measurement', default="KG/acre"
    )
    category = models.ForeignKey(InputCategory, on_delete=models.CASCADE, db_column='Input_product_Input_category_id')
    
    class Meta:
        db_table ='Input_product'
    
    def __str__(self):
        return self.name
    
    
class InputInventory(models.Model):
    id = models.BigAutoField(db_column='Input_Inventory_id',auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField('Input Inventory name', max_length=127, db_column='Input_Inventory_name')
    slug = SlugField(allow_unicode=True)
    desc = models.TextField('Input Inventory description', db_column='Input_Inventory_desc')
    ref_code = models.CharField('Input Inventory reference code', unique=True, blank=True, max_length=36, db_column='Input_Inventory_ref_code')
    created_on = models.DateTimeField('Input Inventory created on', auto_now_add=True, db_column='Input_Inventory_created_on')
    updated_on = models.DateTimeField('Input Inventory updated on', auto_now=True, db_column='Input_Inventory_updated_on')
    
    class Meta:
        db_table = 'Input_Inventory'
    
    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = str(uuid4()).rsplit('-')[-1]
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return '%s - %s' % (self.name, self.ref_code)


class InputInventoryItem(models.Model):
    id = models.BigAutoField(db_column='Input_Inventory_item_id',auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    input_product = models.ForeignKey(
        InputProduct, on_delete=models.CASCADE, 
        db_column='Input_Inventory_item_Input_product_id'
    )
    quantity = models.PositiveIntegerField('Input Inventory item quantity', db_column='Input_Inventory_item_quantity')
    total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    total_cost = MoneyField(amount_field="total_net_amount", currency_field="currency")
    input_inventory = models.ForeignKey(
        InputInventory, on_delete=models.CASCADE, related_name="items",
        db_column='Input_Inventory_item_Input_Inventory_id'
    )
    
    class Meta:
        db_table = 'Input_Inventory_item'
        
    def get_total(self):
        pass
    
    def __str__(self):
        return "%s - %s Inventory Item" %(self.input_product.name, self.input_inventory.name)
