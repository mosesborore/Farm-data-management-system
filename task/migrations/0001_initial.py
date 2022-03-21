# Generated by Django 3.2.4 on 2022-03-19 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farm', '0001_initial'),
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('farming', '0001_initial'),
        ('input', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, db_column='Farm_Task_id', primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Farm_Task_name', max_length=256, verbose_name='Farm Task Name')),
                ('start_date', models.DateTimeField(db_column='Farm_Task_start_date', verbose_name='Farm Task start date')),
                ('deadline', models.DateTimeField(db_column='Farm_Task_deadline', verbose_name='Farm Task end date')),
                ('updated_on', models.DateField(auto_now=True, db_column='Farm_Task_updated_on', verbose_name='Farm Task updated on')),
                ('objective', tinymce.models.HTMLField(db_column='Farm_Task_objectives', verbose_name='Farm objectives')),
                ('notes', tinymce.models.HTMLField(db_column='Farm_Task_notes', verbose_name='Farm Task notes')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('Ongoing', 'ongoing'), ('complete', 'complete'), ('cancelled', 'cancelled')], db_column='Farm_Task_status', max_length=64, verbose_name='Farm Task status')),
                ('currency', models.CharField(blank=True, default='KSH', max_length=3, null=True)),
                ('expected_expenses_price_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('product_units_used', models.PositiveIntegerField(db_column='Farm_Task_Input_product_units_used', default=0, verbose_name='Input product units used')),
                ('created_by', models.ForeignKey(db_column='Farm_Task_created_by', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('farm', models.ForeignKey(db_column='Farm_Task_Farm_id', on_delete=django.db.models.deletion.CASCADE, to='farm.farm')),
                ('farming_season', models.ForeignKey(db_column='Farm_Task_Farming_season_id', on_delete=django.db.models.deletion.CASCADE, to='farming.farmingseason', verbose_name='Farm Task Farming season')),
                ('products', models.ManyToManyField(db_column='Farm_Task_Input_product_id', to='input.InputProduct', verbose_name='Farm Task product to use')),
                ('workers', models.ManyToManyField(db_column='Farm_Task_Worker_id', to='account.Worker', verbose_name='Workers to carry out this task')),
            ],
            options={
                'db_table': 'Farm_Task',
                'ordering': ('-start_date',),
            },
        ),
    ]