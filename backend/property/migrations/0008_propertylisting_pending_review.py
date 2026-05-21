from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_propertylisting_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertylisting',
            name='status',
            field=models.CharField(
                choices=[
                    ('DRAFT', 'Draft'),
                    ('PENDING_REVIEW', 'Pending Review'),
                    ('ACTIVE', 'Active'),
                    ('SOLD', 'Sold'),
                    ('LEASED', 'Leased'),
                    ('UNDER_OFFER', 'Under Offer'),
                    ('INACTIVE', 'Inactive'),
                ],
                default='ACTIVE',
                max_length=20,
                verbose_name='Current Listing Status',
            ),
        ),
    ]
