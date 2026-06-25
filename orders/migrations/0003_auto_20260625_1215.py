from django.db import migrations
import uuid

def generate_order_numbers(apps, schema_editor):

    Order = apps.get_model(
        "orders",
        "Order"
    )

    for order in Order.objects.filter(order_number__isnull=True):

        order.order_number = (
            f"LXC-{uuid.uuid4().hex[:6].upper()}"
        )

        order.save()



class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_order_number"),
    ]

    operations = [
        migrations.RunPython(
            generate_order_numbers
        ),
    ]