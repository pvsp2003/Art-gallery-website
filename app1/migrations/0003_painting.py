# Generated by Django 5.0.3 on 2024-03-31 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_cust'),
    ]

    operations = [
        migrations.CreateModel(
            name='painting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='paintings/')),
                ('name', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=20)),
                ('medium', models.CharField(max_length=20)),
                ('rating', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'painting',
            },
        ),
    ]