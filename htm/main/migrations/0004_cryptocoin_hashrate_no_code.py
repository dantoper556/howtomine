# Generated by Django 4.1.5 on 2023-05-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_cryptocoin'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocoin',
            name='hashrate_no_code',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]
