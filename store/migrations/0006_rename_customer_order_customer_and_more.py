# Generated by Django 4.2.4 on 2023-08-19 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_date_order_order_date_orderd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Customer',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='date_orderd',
            new_name='date_ordered',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='Product',
            new_name='product',
        ),
    ]
