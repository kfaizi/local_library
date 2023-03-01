from django.db import models
from django.urls import reverse
import uuid

class Genre(models.Model):
    """Model for book genre."""
    name = models.CharField(max_length=100, help_text='Enter a book genre')

    def __str__(self):
        """String representing the Model object."""
        return self.name

class Language(models.Model):
    """Model for a written language."""
    name = models.CharField(max_length=100, help_text='Enter the language in which this copy of the book is written.')

    def __str__(self):
        return self.name

class Book(models.Model):
    """Model for a Book."""
    title = models.CharField(max_length=100)
    author = models.ManyToManyField('Author')
    summary = models.TextField(max_length=500, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13-character ISBN reference number')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for the book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns URL for a detailed book record."""
        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):
        """For displaying the author(s) in Admin."""
        authors = []
        for i in self.author.all():
            full_name = str(i.last_name) + ', ' + str(i.first_name)
            authors.append(full_name)

        return '; '.join(i for i in authors)

    display_author.short_description = 'Author(s)'

    def display_genre(self):
        """For displaying the genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Model for a specific physical copy of a book."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this copy')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=100)
    due_date = models.DateField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('l', 'Loaned'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model for a specific author."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns URL for an author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

