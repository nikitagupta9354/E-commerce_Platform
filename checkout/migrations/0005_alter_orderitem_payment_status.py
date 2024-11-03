# Generated by Django 5.1.2 on 2024-11-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_orderitem_payment_status_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='payment_status',
            field=models.CharField(choices=[('Success', 'Success'), ('Refund Demanded', 'Refund Demanded'), ('Refund Processed', 'Refund Processed')], default='Success', max_length=20),
        ),
    ]
