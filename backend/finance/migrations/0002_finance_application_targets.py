from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_property_module_expansion'),
        ('projects', '0005_alter_investmentcommitment_options_and_more'),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeapplication',
            name='target_type',
            field=models.CharField(choices=[('PROPERTY', 'Property'), ('PROJECT', 'Project'), ('MATERIAL_ORDER', 'Material Order'), ('CONTRACT', 'Contract'), ('GENERAL_WORKING_CAPITAL', 'General Working Capital')], default='GENERAL_WORKING_CAPITAL', max_length=30),
        ),
        migrations.AddField(
            model_name='financeapplication',
            name='purpose_category',
            field=models.CharField(choices=[('ACQUISITION', 'Acquisition'), ('COMPLETION', 'Completion'), ('RENOVATION', 'Renovation'), ('MATERIALS_PROCUREMENT', 'Materials Procurement'), ('WORKING_CAPITAL', 'Working Capital')], default='WORKING_CAPITAL', max_length=30),
        ),
        migrations.AddField(
            model_name='financeapplication',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='finance_applications', to='projects.project'),
        ),
        migrations.AddField(
            model_name='financeapplication',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='finance_applications', to='property.propertylisting'),
        ),
    ]
