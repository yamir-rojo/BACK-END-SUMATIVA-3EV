from django.db import migrations


def crear_grupo_cocina(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias

    permisos = []
    for modelo in ('linea', 'producto', 'encargo'):
        content_type, _ = ContentType.objects.using(db_alias).get_or_create(
            app_label='catalogo',
            model=modelo,
        )
        acciones = ('view',) if modelo == 'encargo' else ('view', 'add', 'change')
        for accion in acciones:
            permiso, _ = Permission.objects.using(db_alias).get_or_create(
                content_type=content_type,
                codename=f'{accion}_{modelo}',
                defaults={'name': f'Can {accion} {modelo}'},
            )
            permisos.append(permiso)

    grupo, _ = Group.objects.using(db_alias).get_or_create(name='Cocina')
    grupo.permissions.set(permisos)


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0002_alter_producto_fotografia'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(crear_grupo_cocina, migrations.RunPython.noop),
    ]
