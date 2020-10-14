# Generated by Django 3.1.1 on 2020-10-12 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiques', '0002_auto_20201011_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recherche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu_recherche', models.CharField(max_length=255, verbose_name='Contenu de la recherche')),
                ('compteur_recherche', models.IntegerField(default=0, verbose_name='Nombre de fois')),
            ],
        ),
    ]