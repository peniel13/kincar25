# Generated by Django 5.1.3 on 2024-11-30 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('name', models.CharField(max_length=100)),
                ('website_link', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
