# Generated by Django 4.2.4 on 2023-08-29 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_delivery_carrier_delivery_tracking_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]
