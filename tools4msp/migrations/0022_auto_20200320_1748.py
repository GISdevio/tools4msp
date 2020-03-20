# Generated by Django 2.2.2 on 2020-03-20 17:48

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tools4msp', '0021_casestudy_gridinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casestudy',
            name='gridinfo',
        ),
        migrations.AddField(
            model_name='casestudylayer',
            name='layerinfo',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
