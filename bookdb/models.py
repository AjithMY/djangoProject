from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    total_books = models.IntegerField(default=0)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.area})"


class Author(models.Model):
    name = models.CharField(max_length=200)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Availability(models.Model):
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.status


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    description = models.TextField()
    published_year = models.IntegerField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.title
