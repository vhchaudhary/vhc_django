# Generated by Django 2.1.1 on 2018-10-09 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(unique=True)),
                ('brochure', models.FileField(upload_to='')),
                ('email', models.EmailField(max_length=35)),
                ('address', models.TextField(max_length=60)),
                ('contact_no', models.CharField(max_length=13)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fee_type', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fees_management.Branch')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(unique=True)),
                ('logo', models.BinaryField()),
                ('email', models.EmailField(max_length=35)),
                ('contact_no', models.CharField(max_length=13)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('enr_no', models.CharField(max_length=10, unique=True, verbose_name='Enrollment No')),
                ('address', models.TextField(max_length=60)),
                ('contact_no', models.CharField(max_length=13)),
                ('dob', models.DateField(verbose_name='Date Of Birth')),
                ('branch', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fees_management.Branch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fees_management.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('paid_amount', models.FloatField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], max_length=10)),
                ('request_dump', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='branch',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fees_management.Institute'),
        ),
    ]