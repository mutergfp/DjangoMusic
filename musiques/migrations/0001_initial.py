# Generated by Django 3.1.1 on 2020-10-08 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_album', models.CharField(max_length=100, verbose_name="Nom de la l'album")),
                ('type_album', models.CharField(choices=[('EP', 'EP'), ('AL', 'Album'), ('SG', 'Single')], max_length=6, verbose_name="Type de l'album")),
                ('image_album', models.ImageField(default='assets/default/img_album_default.jpg', upload_to='assets/img_artistes', verbose_name="Image de l'album")),
                ('date_publication_album', models.DateField(null=True, verbose_name="Date de parution de l'album")),
            ],
        ),
        migrations.CreateModel(
            name='Artiste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_artiste', models.CharField(max_length=255, verbose_name="Nom de l'artiste")),
                ('description_artiste', models.TextField(null=True, verbose_name="Description de l'artiste")),
                ('image_artiste', models.ImageField(default='assets/default/img_artiste_default.jpg', null=True, upload_to='assets/img_albums', verbose_name="Image de l'artiste")),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_genre', models.CharField(max_length=100, verbose_name='Nom du genre')),
                ('description_genre', models.CharField(max_length=50, verbose_name='Description du genre')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_label', models.CharField(max_length=100, verbose_name='Nom du Label')),
                ('description_label', models.TextField(null=True, verbose_name='Description du Label')),
            ],
        ),
        migrations.CreateModel(
            name='Musique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre_musique', models.CharField(max_length=255, verbose_name='Titre de la musique')),
                ('duree_musique', models.TimeField(verbose_name='Durée de la musique')),
                ('id_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='musiques.album', verbose_name='Album de la musiques')),
                ('id_artiste', models.ManyToManyField(to='musiques.Artiste', verbose_name='Artiste(s) de la musique')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='id_artiste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musiques.artiste', verbose_name="Artiste de l'album"),
        ),
        migrations.AddField(
            model_name='album',
            name='id_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musiques.genre', verbose_name="Genre de l'album"),
        ),
        migrations.AddField(
            model_name='album',
            name='id_label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musiques.label', verbose_name="Label de l'album"),
        ),
    ]
