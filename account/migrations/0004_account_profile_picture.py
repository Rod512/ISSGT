# Generated by Django 5.1.2 on 2024-12-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/user'),
        ),
    ]
