# Generated by Django 4.1.7 on 2023-09-27 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0011_compracabecera_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoproducto',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='compras.categoria'),
        ),
    ]
