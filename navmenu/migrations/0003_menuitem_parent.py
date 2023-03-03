# Generated by Django 4.1.7 on 2023-03-03 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("navmenu", "0002_menuitem_menu_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="navmenu.menuitem",
            ),
        ),
    ]