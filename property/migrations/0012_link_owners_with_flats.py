from django.db import migrations


def link_owners_with_flats(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')
    Ownership = Owner.flats.through

    owner_ids = {
        (owner.full_name, owner.phonenumber): owner.id
        for owner in Owner.objects.all()
    }

    links = []

    for flat in Flat.objects.all().iterator():
        owner_key = (flat.owner, flat.owners_phonenumber)
        owner_id = owner_ids.get(owner_key)

        if owner_id is None:
            owner, _ = Owner.objects.get_or_create(
                full_name=flat.owner,
                phonenumber=flat.owners_phonenumber,
                defaults={
                    'pure_phone': flat.owner_pure_phone,
                },
            )
            owner_id = owner.id
            owner_ids[owner_key] = owner_id

        links.append(
            Ownership(
                owner_id=owner_id,
                flat_id=flat.id,
            )
        )

    Ownership.objects.bulk_create(links, ignore_conflicts=True)


def rollback_owners_links(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')
    Ownership = Owner.flats.through

    Ownership.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0011_fill_owners'),
    ]

    operations = [
        migrations.RunPython(link_owners_with_flats, rollback_owners_links),
    ]