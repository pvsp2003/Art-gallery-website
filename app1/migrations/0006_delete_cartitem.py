# Generated by Django 5.0.3 on 2024-03-31 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_cartitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]