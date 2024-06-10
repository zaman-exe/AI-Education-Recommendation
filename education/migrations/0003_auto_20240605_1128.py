# Generated by Django 3.0.5 on 2024-06-05 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20240605_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counsellor',
            name='department',
            field=models.CharField(choices=[('O level Counseling', 'O level Counseling'), ('A level Counseling', 'A level Counseling'), ('Matric Science level Counseling', 'Matric Science level Counseling'), ('Fsc Pre-Medical Counseling', 'Fsc Pre-Medical Counseling'), ('Fsc Pre-Engineering Counseling', 'Fsc Pre-Engineering Counseling'), ('ICS Counseling', 'ICS Counseling')], default='A level Counseling', max_length=50),
        ),
    ]