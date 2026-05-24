from django.db import migrations
import phonenumbers


def fill_owner_pure_phone(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    for flat in Flat.objects.all():
        try:
            parsed_phone = phonenumbers.parse(flat.owners_phonenumber, 'RU')
        except phonenumbers.NumberParseException:
            continue

        if not phonenumbers.is_valid_number(parsed_phone):
            continue

        flat.owner_pure_phone = phonenumbers.format_number(
            parsed_phone,
            phonenumbers.PhoneNumberFormat.E164,
        )
        flat.save(update_fields=['owner_pure_phone'])


def rollback_owner_pure_phone(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Flat.objects.update(owner_pure_phone='')


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(fill_owner_pure_phone, rollback_owner_pure_phone),
    ]