# Generated by Django 3.0.3 on 2020-02-29 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub', '0003_auto_20200229_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adopt',
            name='pictures',
            field=models.ImageField(upload_to='pictures'),
        ),
    ]