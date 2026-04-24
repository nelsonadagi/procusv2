from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chatattachment_message'),
        ('property', '0003_propertylisting_country_and_more'),
        ('projects', '0005_alter_investmentcommitment_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='propertylisting',
            name='appointment_enabled',
            field=models.BooleanField(default=True, verbose_name='Appointments Enabled'),
        ),
        migrations.AddField(
            model_name='propertylisting',
            name='financing_allowed',
            field=models.BooleanField(default=False, verbose_name='Financing Allowed'),
        ),
        migrations.AddField(
            model_name='propertylisting',
            name='inquiry_enabled',
            field=models.BooleanField(default=True, verbose_name='Inquiries Enabled'),
        ),
        migrations.AddField(
            model_name='propertylisting',
            name='listing_type',
            field=models.CharField(choices=[('SALE', 'Sale'), ('LEASE', 'Lease'), ('DEVELOPMENT_OPPORTUNITY', 'Development Opportunity'), ('COMPLETED_PROJECT', 'Completed Project')], default='SALE', max_length=30, verbose_name='Listing Type'),
        ),
        migrations.AddField(
            model_name='propertylisting',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_properties', to=settings.AUTH_USER_MODEL, verbose_name='Property Manager'),
        ),
        migrations.AddField(
            model_name='propertylisting',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='asset_type',
            field=models.CharField(choices=[('LAND', 'Land'), ('RESIDENTIAL', 'Residential'), ('COMMERCIAL', 'Commercial'), ('INDUSTRIAL', 'Industrial'), ('MIXED_USE', 'Mixed Use'), ('HOSPITALITY', 'Hospitality'), ('RENOVATION', 'Renovation'), ('SPECIAL_PURPOSE', 'Special Purpose')], max_length=20, verbose_name='Type of Asset'),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('SOLD', 'Sold'), ('LEASED', 'Leased'), ('UNDER_OFFER', 'Under Offer'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=20, verbose_name='Current Listing Status'),
        ),
        migrations.AddField(
            model_name='developmentmetadata',
            name='development_stage',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='developmentmetadata',
            name='estimated_completion_budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='developmentmetadata',
            name='expected_completion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='developmentmetadata',
            name='recommended_use',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.CreateModel(
            name='PropertyAvailabilityWindow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('recurrence_rule', models.CharField(blank=True, default='', max_length=100)),
                ('slot_duration_minutes', models.PositiveIntegerField(default=60)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('managed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_availability_windows', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability_windows', to='property.propertylisting')),
            ],
            options={'ordering': ['start_at']},
        ),
        migrations.CreateModel(
            name='PropertyInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inquiry_type', models.CharField(choices=[('GENERAL', 'General'), ('VIEWING', 'Viewing'), ('FINANCING', 'Financing'), ('PARTNERSHIP', 'Partnership'), ('MATERIALS', 'Materials'), ('SERVICE', 'Service')], default='GENERAL', max_length=20)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('preferred_contact_method', models.CharField(blank=True, default='', max_length=20)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('NEW', 'New'), ('CONTACTED', 'Contacted'), ('QUALIFIED', 'Qualified'), ('CLOSED', 'Closed'), ('SPAM', 'Spam')], default='NEW', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chat_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_inquiries', to='chat.chatroom')),
                ('inquirer_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_inquiries', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='property.propertylisting')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('scheduled_start', models.DateTimeField()),
                ('scheduled_end', models.DateTimeField()),
                ('notes', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('REQUESTED', 'Requested'), ('CONFIRMED', 'Confirmed'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('NO_SHOW', 'No Show')], default='REQUESTED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('availability_window', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='property.propertyavailabilitywindow')),
                ('chat_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_appointments', to='chat.chatroom')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_property_appointments', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='property.propertylisting')),
                ('visitor_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_appointments', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['scheduled_start']},
        ),
    ]
