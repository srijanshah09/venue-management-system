# Generated by Django 4.1.7 on 2023-04-11 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("venues", "0002_alter_city_options_alter_address_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="availability",
            name="venue",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="days",
                to="venues.venue",
            ),
        ),
    ]