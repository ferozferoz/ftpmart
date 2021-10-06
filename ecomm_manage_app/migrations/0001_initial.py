# Generated by Django 3.1.7 on 2021-09-20 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='ecomm_manage_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_policy_type', models.CharField(max_length=200)),
                ('return_policy_desc', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('home_phone', models.CharField(max_length=15)),
                ('office_phone', models.CharField(max_length=15)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warranty_type', models.CharField(max_length=200)),
                ('warranty_desc', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('sell_quantity', models.CharField(max_length=200)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('display_original_selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('display_new_selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('image_1', models.ImageField(upload_to='products/images/')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='products/images/')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='products/images/')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='products/images/')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='products/images/')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='ecomm_manage_app.category')),
                ('return_policy', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ecomm_manage_app.returnpolicy')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='ecomm_manage_app.category')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm_manage_app.supplier')),
                ('warranty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ecomm_manage_app.warranty')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='admins')),
                ('mobile', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
