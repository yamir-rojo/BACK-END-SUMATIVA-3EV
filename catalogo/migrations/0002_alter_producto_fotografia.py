from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto",
            name="fotografia",
            field=models.ImageField(upload_to="productos/"),
        ),
    ]
