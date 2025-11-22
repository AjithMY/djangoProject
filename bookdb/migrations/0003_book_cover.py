from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookdb', '0002_populate_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(upload_to='covers/', null=True, blank=True),
        ),
    ]
