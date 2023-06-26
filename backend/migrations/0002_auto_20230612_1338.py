# Generated by Django 3.2.19 on 2023-06-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chargingstation',
            name='is_available',
        ),
        migrations.AddField(
            model_name='chargingstation',
            name='is_fuctional',
            field=models.BooleanField(default=True, help_text='Verify if the station is functional'),
        ),
        migrations.AddField(
            model_name='chargingstation',
            name='is_occupied',
            field=models.BooleanField(default=False, help_text='Verify if the station is Currently available for use'),
        ),
        migrations.AlterField(
            model_name='chargingstation',
            name='battery_capacity',
            field=models.DecimalField(decimal_places=2, help_text='Current Battery level OF storage', max_digits=5),
        ),
        migrations.AlterField(
            model_name='chargingstation',
            name='charging_speed',
            field=models.DecimalField(choices=[('Level 1', 2.3), ('Level 2', 9), ('DC Fast Charging', 60)], decimal_places=2, help_text='level 1,level2 or fast charging', max_digits=5),
        ),
        migrations.AlterField(
            model_name='chargingstation',
            name='solar_intensity',
            field=models.DecimalField(decimal_places=2, help_text='Solar intensity for a 16 day period using lon and lat values', max_digits=5),
        ),
        migrations.AlterField(
            model_name='chargingstation',
            name='solar_panel_capacity',
            field=models.DecimalField(decimal_places=2, help_text='Stations solar capacity.', max_digits=6),
        ),
        migrations.AlterField(
            model_name='chargingstation',
            name='solar_panel_efficiency',
            field=models.DecimalField(decimal_places=2, help_text='Standard ', max_digits=4),
        ),
    ]