# Generated by Django 4.0.1 on 2022-02-08 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_rename_other_bill_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]