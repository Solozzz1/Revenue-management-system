# Generated by Django 4.2.16 on 2024-10-01 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaxInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('penalty', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('interest', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('P', 'Paid'), ('U', 'Unpaid'), ('O', 'Overdue'), ('PP', 'Partially Paid')], default='U', max_length=2)),
                ('tax_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tax.taxtype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_reference', models.CharField(max_length=255)),
                ('payment_method', models.CharField(choices=[('CC', 'Credit Card'), ('BT', 'Bank Transfer'), ('PP', 'PayPal'), ('MP', 'Mobile Payment')], max_length=2)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tax.taxinvoice')),
            ],
        ),
    ]
