# Generated by Django 5.0 on 2023-12-29 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_player_betthisround_player_folded_table_pot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='shoved',
            field=models.BooleanField(default=False),
        ),
    ]