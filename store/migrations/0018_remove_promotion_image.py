# Generated by Django 4.2.4 on 2023-08-31 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_promotion_description_remove_promotion_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='image',
        ),
    ]