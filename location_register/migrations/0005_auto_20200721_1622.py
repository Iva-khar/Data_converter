# Generated by Django 3.0.7 on 2020-07-21 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('location_register', '0004_auto_20200630_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='KoatuuCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KoatuuRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('code', models.CharField(max_length=10, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='District',
            new_name='RatuDistrict',
        ),
        migrations.RenameModel(
            old_name='Region',
            new_name='RatuRegion',
        ),
        migrations.RenameModel(
            old_name='Street',
            new_name='RatuStreet',
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='KoatuuCategory',
        ),
        migrations.RenameModel(
            old_name='City',
            new_name='RatuCity',
        ),
        migrations.RenameModel(
            old_name='CityDistrict',
            new_name='RatuCityDistrict',
        ),
        migrations.CreateModel(
            name='KoatuuDistrict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, null=True, unique=True)),
                ('region',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='location_register.KoatuuRegion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KoatuuCityDistrict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, null=True, unique=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='location_register.KoatuuCategory')),
                ('city',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='location_register.KoatuuCity')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='location_register.KoatuuDistrict')),
                ('region',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='location_register.KoatuuRegion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='koatuucity',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='location_register.KoatuuCategory'),
        ),
        migrations.AddField(
            model_name='koatuucity',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='location_register.KoatuuDistrict'),
        ),
        migrations.AddField(
            model_name='koatuucity',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='location_register.KoatuuRegion'),
        ),
        migrations.AlterField(
            model_name='ratucity',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='location_register.KoatuuCategory'),
        ),
        migrations.AlterField(
            model_name='ratucitydistrict',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='location_register.KoatuuCategory'),
        ),
    ]
