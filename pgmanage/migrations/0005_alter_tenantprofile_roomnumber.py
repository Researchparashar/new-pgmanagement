# Generated by Django 5.1.4 on 2024-12-24 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgmanage', '0004_alter_tenantprofile_moveindate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantprofile',
            name='roomNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
