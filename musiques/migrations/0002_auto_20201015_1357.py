# Generated by Django 3.1.1 on 2020-10-15 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiques', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artiste',
            name='description_artiste',
            field=models.TextField(default='Pas de description disponnible pour cet artiste.', null=True, verbose_name="Description de l'artiste"),
        ),
        migrations.AlterField(
            model_name='artiste',
            name='image_artiste',
            field=models.ImageField(default='/assets/default/img_artiste_default-min.jpg', null=True, upload_to='assets/img_albums', verbose_name="Image de l'artiste"),
        ),
    ]
