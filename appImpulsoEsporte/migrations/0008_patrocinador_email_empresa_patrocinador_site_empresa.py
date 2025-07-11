# Generated by Django 5.0.14 on 2025-07-06 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appImpulsoEsporte', '0007_remove_patrocinador_aberto_para_oportunidades'),
    ]

    operations = [
        migrations.AddField(
            model_name='patrocinador',
            name='email_empresa',
            field=models.EmailField(blank=True, help_text='E-mail corporativo da empresa', max_length=254, null=True, verbose_name='E-mail da empresa'),
        ),
        migrations.AddField(
            model_name='patrocinador',
            name='site_empresa',
            field=models.URLField(blank=True, help_text='Website oficial da empresa', null=True, verbose_name='Site da empresa'),
        ),
    ]
