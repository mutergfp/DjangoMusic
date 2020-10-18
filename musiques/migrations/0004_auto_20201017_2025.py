# Generated by Django 3.1.1 on 2020-10-17 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musiques', '0003_auto_20201017_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_genre', models.CharField(max_length=100, verbose_name='Nom du genre')),
                ('description_genre', models.CharField(max_length=50, verbose_name='Description du genre')),
            ],
        ),
        migrations.AlterField(
            model_name='album',
            name='type_album',
            field=models.CharField(max_length=6, verbose_name="Type de l'album"),
        ),
        migrations.AddField(
            model_name='album',
            name='id_genre',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='musiques.genre', verbose_name="Genre de l'album"),
            preserve_default=False,
        ),
    ]
