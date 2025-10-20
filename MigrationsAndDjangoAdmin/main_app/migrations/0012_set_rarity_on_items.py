from django.db import migrations

def set_rarity(apps, schema_editor):
    Item = apps.get_model('main_app', 'Item')
    for item in Item.objects.all():
        if item.price < 10:
            item.rarity = "Rare"
        elif item.price <= 20:
            item.rarity = "Very Rare"
        elif item.price <= 30:
            item.rarity = "Extremely Rare"
        else:
            item.rarity = "Mega Rare"
        item.save()

def reverse_rarity(apps, schema_editor):
    Item = apps.get_model('main_app', 'Item')
    default_rarity = Item._meta.get_field('rarity').default
    for item in Item.objects.all():
        item.rarity = default_rarity
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_rarity, reverse_rarity)
    ]