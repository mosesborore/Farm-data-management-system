# Generated by Django 3.2.4 on 2022-03-19 18:06

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InputCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, db_column='Input_category_id', primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Input_category_name', max_length=256, verbose_name='Input Category name')),
                ('desc', tinymce.models.HTMLField(db_column='Input_category_desc', verbose_name='Input Category description')),
            ],
            options={
                'db_table': 'Input_category',
            },
        ),
        migrations.CreateModel(
            name='InputInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, db_column='Input_Inventory_id', primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Input_Inventory_name', max_length=127, verbose_name='Input Inventory name')),
                ('desc', models.TextField(db_column='Input_Inventory_desc', verbose_name='Input Inventory description')),
                ('ref_code', models.CharField(blank=True, db_column='Input_Inventory_ref_code', max_length=36, unique=True, verbose_name='Input Inventory reference code')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='Input_Inventory_created_on', verbose_name='Input Inventory created on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='Input_Inventory_updated_on', verbose_name='Input Inventory updated on')),
            ],
            options={
                'db_table': 'Input_Inventory',
            },
        ),
        migrations.CreateModel(
            name='InputProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, db_column='Input_product_id', primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Input_product_name', max_length=256, verbose_name='Product name')),
                ('desc', models.TextField(db_column='Input_product_desc', verbose_name='Input product description')),
                ('currency', models.CharField(blank=True, default='KSH', max_length=3, null=True)),
                ('unit_price_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_units', models.PositiveBigIntegerField(db_column='Input_product_total_cost', verbose_name='Product total units')),
                ('total_net_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('unit_weight', models.PositiveIntegerField(db_column='Input_product_unit_weight', verbose_name='Product unit weight')),
                ('unit_measurement', models.CharField(choices=[('KG', 'kilograms'), ('G', 'grams'), ('L', 'liter'), ('BAG', 'bag')], db_column='Input_product_unit_measurement', max_length=5, verbose_name='Product unit measurement')),
                ('unit_rate', models.PositiveIntegerField(db_column='Input_product_unit_rate', verbose_name='Product unit rate (rate at which it is used)')),
                ('unit_rate_measurement', models.CharField(choices=[('KG/acre', 'kilogram/acre'), ('L/acre', 'liter/acre'), ('G/acre', 'grams/acre'), ('KG/ha', 'kilogram/hectare'), ('L/ha', 'liter/hectare'), ('G/hectare', 'grams/hectare')], db_column='Input_product_unit_rate_measurement', max_length=32, verbose_name='Product unit rate measurement')),
                ('category', models.ForeignKey(db_column='Input_product_Input_category_id', on_delete=django.db.models.deletion.CASCADE, to='input.inputcategory')),
            ],
            options={
                'db_table': 'Input_product',
            },
        ),
        migrations.CreateModel(
            name='InputInventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, db_column='Input_Inventory_item_id', primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(db_column='Input_Inventory_item_quantity', verbose_name='Input Inventory item quantity')),
                ('total_net_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('input_inventory_id', models.ForeignKey(db_column='Input_Inventory_item_Input_Inventory_id', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='input.inputinventory')),
                ('input_product_id', models.ForeignKey(db_column='Input_Inventory_item_Input_product_id', on_delete=django.db.models.deletion.CASCADE, to='input.inputproduct')),
            ],
            options={
                'db_table': 'Input_Inventory_item',
            },
        ),
    ]
