# Generated by Django 5.1.3 on 2024-12-02 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamentos', '0002_webhooklog_delete_mercadopagowebhooklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhooklog',
            name='corpo_bruto',
            field=models.TextField(blank=True, null=True),
        ),
    ]
