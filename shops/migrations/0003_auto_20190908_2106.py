# Generated by Django 2.2.5 on 2019-09-08 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_auto_20190906_1943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cities'},
        ),
        migrations.AlterUniqueTogether(
            name='shop',
            unique_together={('name', 'city', 'street', 'building_number')},
        ),
    ]
