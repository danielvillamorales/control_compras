# Generated by Django 4.1.7 on 2023-09-11 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_alter_compracabecera_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compradetalle',
            name='Categoria',
        ),
        migrations.AddField(
            model_name='compradetalle',
            name='tipo_producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='compras.tipoproducto'),
        ),
    ]