# Generated by Django 5.0.1 on 2024-04-20 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_account_delete_mehdi_alter_post_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='age',
        ),
        migrations.AlterField(
            model_name='account',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]