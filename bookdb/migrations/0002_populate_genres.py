from django.db import migrations


def create_genres(apps, schema_editor):
    Genre = apps.get_model('bookdb', 'Genre')
    genres = [
        'Fiction',
        'Non-Fiction',
        'Mystery / Thriller',
        'Fantasy',
        'Science Fiction (Sci-Fi)',
        'Romance',
        'Horror',
        'Historical Fiction',
        'Biography / Autobiography',
        'Self-Help / Motivation',
    ]
    for name in genres:
        Genre.objects.get_or_create(name=name)


def remove_genres(apps, schema_editor):
    Genre = apps.get_model('bookdb', 'Genre')
    names = [
        'Fiction',
        'Non-Fiction',
        'Mystery / Thriller',
        'Fantasy',
        'Science Fiction (Sci-Fi)',
        'Romance',
        'Horror',
        'Historical Fiction',
        'Biography / Autobiography',
        'Self-Help / Motivation',
    ]
    Genre.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bookdb', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_genres, remove_genres),
    ]
