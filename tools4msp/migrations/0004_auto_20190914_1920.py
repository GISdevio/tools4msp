# Generated by Django 2.2.2 on 2019-09-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools4msp', '0003_auto_20190718_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='casestudyinput',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='casestudylayer',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='casestudyruninput',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='casestudyrunlayer',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='casestudyrunoutput',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='casestudyrunoutputlayer',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='codedlabel',
            name='code',
            field=models.SlugField(max_length=10, unique=True),
        ),
    ]
