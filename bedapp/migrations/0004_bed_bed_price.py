# Generated by Django 4.2.7 on 2024-03-12 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bedapp', '0003_hostel_room_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='bed',
            name='bed_price',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
