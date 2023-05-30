# Generated by Django 4.2.1 on 2023-05-23 11:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(max_length=120)),
                ('username', models.CharField(db_index=True, max_length=50, unique=True)),
                ('pezeshki_code', models.IntegerField(blank=True, null=True, verbose_name='شماره نظام پزشکی')),
                ('email', models.EmailField(blank=True, default=None, max_length=50, null=True)),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='موبایل')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='last login')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pezeshki_code', models.IntegerField(blank=True, null=True, verbose_name='شماره نظام پزشکی')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('working_hour', models.TextField(max_length=120, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('birth_year', models.TextField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('expertise', models.ManyToManyField(to='accounts.expertise')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('expertise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.expertise')),
            ],
        ),
    ]