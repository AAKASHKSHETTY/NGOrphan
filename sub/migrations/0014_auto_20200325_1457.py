# Generated by Django 3.0.3 on 2020-03-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub', '0013_delete_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adopt',
            name='mes',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
