# Generated by Django 3.1.1 on 2020-10-15 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musiques', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image_album',
            field=models.ImageField(default='/assets/default/img_album_default-min.jpg', upload_to='assets/img_artistes', verbose_name="Image de l'album"),
        ),
        migrations.AlterField(
            model_name='artiste',
            name='image_artiste',
            field=models.ImageField(default='/assets/default/img_artiste_default-min.jpg', null=True, upload_to='assets/img_albums', verbose_name="Image de l'artiste"),
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_musique', models.ManyToManyField(to='musiques.Musique', verbose_name='Musique de la playlist')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur de la playlist')),
            ],
        ),
    ]