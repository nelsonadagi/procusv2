from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0008_propertylisting_pending_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertymediaasset',
            name='document_category',
            field=models.CharField(
                blank=True,
                choices=[
                    ('GENERAL', 'General'),
                    ('DEED', 'Title Deed'),
                    ('FLOOR_PLAN', 'Floor Plan'),
                    ('COMPLIANCE', 'Compliance Certificate'),
                    ('SURVEY', 'Survey'),
                    ('VALUATION', 'Valuation'),
                    ('BROCHURE', 'Brochure'),
                ],
                default='',
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name='PropertyInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('full_name', models.CharField(blank=True, default='', max_length=255)),
                ('reason', models.CharField(blank=True, default='availability', max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to='property.propertylisting')),
            ],
            options={
                'unique_together': {('property', 'email', 'reason')},
            },
        ),
        migrations.CreateModel(
            name='SavedPropertySearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('name', models.CharField(blank=True, default='Property search', max_length=255)),
                ('filters', models.JSONField(blank=True, default=dict)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saved_property_searches', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PropertyEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[
                    ('PROPERTY_CREATED', 'Property Created'),
                    ('PUBLISHED', 'Published'),
                    ('INQUIRY_RECEIVED', 'Inquiry Received'),
                    ('INQUIRY_REPLIED', 'Inquiry Replied'),
                    ('SLOT_ADDED', 'Slot Added'),
                    ('VISIT_BOOKED', 'Visit Booked'),
                    ('VISIT_UPDATED', 'Visit Updated'),
                    ('FINANCE_REVIEW_STARTED', 'Finance Review Started'),
                    ('PROJECT_LINKED', 'Project Linked'),
                    ('MODERATION_UPDATED', 'Moderation Updated'),
                    ('ARCHIVED', 'Archived'),
                ], max_length=40)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField(blank=True, default='')),
                ('data', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_events', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='property.propertylisting')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
