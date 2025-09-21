from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genere (e.g Science Fictions French Poetry etc.)",
        unique = True,
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("genere-detail", args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name'],
                name = 'unique_genere_name_unique',
                violation_error_message = 'Genere with this name already exits.',
            ),

            # UniqueConstraint(
            #     Lower('name'),
            #     name = 'unique_genere_name_insensitive_unique',
            #     voilation_error_message = 'Genere with this name already exits.',
            # ),
        ]


class Language(models.Model):
    language = models.CharField(
        max_length=20,
        help_text="Enter the book's natural language (e.g English, French, Japanese etc.)",
        unique=True,
    )

    def __str__(self):
        return self.language


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        help_text = "Enter the book title",
    )

    author = models.ForeignKey(
        "Author",
        on_delete=models.RESTRICT,
        null=True,
    )

    summary = models.TextField(
        max_length=1000,
        help_text = "Enter a brief description of the book",
        null=True,
    )

    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique = True,
        help_text= "13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>",
    )

    genre = models.ManyToManyField(
        Genre,
        help_text = "Select a genre for this book",
    )

    language = models.ForeignKey(
        Language,
        on_delete=models.RESTRICT,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])



class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this paticular book across whole library",
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.RESTRICT,
        null=True,
    )

    imprint = models.CharField(max_length=200)

    due_back = models.DateField(
        null=True,
        blank=True,
    )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        null=True,
        default='m',
        help_text="Book avilability",
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.book.id)])
    
    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)



class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse("author-detail" , args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name})' 
    
