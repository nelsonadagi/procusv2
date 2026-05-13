from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_productinventorymovement'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(default='KES', help_text='ISO 4217 currency code for all listed prices', max_length=10, verbose_name='Currency'),
        ),
    ]
