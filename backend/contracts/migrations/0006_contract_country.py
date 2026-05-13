# Generated manually — adds country FK to Contract model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_alter_contract_eligibility_criteria_and_more'),
        ('platform_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='country',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='contracts',
                to='platform_settings.country',
                verbose_name='Country',
            ),
        ),
    ]
