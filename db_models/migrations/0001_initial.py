# Generated by Django 5.0.6 on 2024-06-17 09:17

import db_models.help
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('products_count', models.IntegerField(default=0)),
                ('photo', models.ImageField(upload_to=db_models.help.SaveMediaFile.category)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'category',
                'ordering': ['id'],
                'indexes': [models.Index(fields=['id'], name='db_models_c_id_4463f2_idx')],
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comments',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('manufacturer_name', models.CharField(max_length=100)),
                ('discount', models.FloatField(default=0)),
                ('image', models.ImageField(upload_to=db_models.help.SaveMediaFile.product)),
                ('popular_products', models.IntegerField(default=0)),
                ('price', models.FloatField()),
                ('price_type', models.CharField(choices=[('$', '$'), ("so'm", "SO'M")], default='$', max_length=10)),
                ('rating', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_models.category')),
                ('comments', models.ManyToManyField(blank=True, to='db_models.comments')),
            ],
            options={
                'verbose_name': 'products',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_number', models.IntegerField(default=1)),
                ('payment_status', models.BooleanField(default=False)),
                ('total_price', models.FloatField(default=0)),
                ('price_type', models.CharField(max_length=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db_models.product')),
            ],
            options={
                'verbose_name': 'cart',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'status',
                'ordering': ['id'],
                'indexes': [models.Index(fields=['id'], name='db_models_s_id_1663d3_idx')],
            },
        ),
        migrations.CreateModel(
            name='OurTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=db_models.help.SaveMediaFile.employee)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_models.status')),
            ],
            options={
                'verbose_name': 'our_team',
                'ordering': ['id'],
            },
        ),
        migrations.AddIndex(
            model_name='comments',
            index=models.Index(fields=['id'], name='db_models_c_id_0624d6_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id'], name='db_models_p_id_69a7f5_idx'),
        ),
        migrations.AddIndex(
            model_name='cart',
            index=models.Index(fields=['id'], name='db_models_c_id_b39151_idx'),
        ),
        migrations.AddIndex(
            model_name='ourteam',
            index=models.Index(fields=['id'], name='db_models_o_id_3cf504_idx'),
        ),
    ]