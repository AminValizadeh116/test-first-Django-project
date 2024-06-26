# Generated by Django 5.0.3 on 2024-03-19 09:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('updated_time', models.DateTimeField(auto_now_add=True)),
                ('reading_time', models.PositiveIntegerField()),
                ('slug', models.SlugField()),
                ('status', models.CharField(choices=[('DR', 'DRAFT'), ('RJ', 'REJECTED'), ('PB', 'PUBLISHED')], default='PB', max_length=120)),
                ('category', models.CharField(choices=[('programming language', 'programming language'), ('AI', 'AI'), ('frontend', 'frontend'), ('backend', 'backend'), ('security', 'security'), ('others', 'others')], max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['status'],
            },
        ),
    ]
