from django import forms
from .models import Book, Genre
import datetime


class BookForm(forms.ModelForm):
    # Author, Library, Availability remain free-text (created if missing).
    # Genre is now a select populated from existing Genre records.
    author_name = forms.CharField(max_length=200, required=True, label='Author')
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=True, label='Genre')
    library_name = forms.CharField(max_length=200, required=True, label='Library')
    AVAILABILITY_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    availability_status = forms.ChoiceField(choices=AVAILABILITY_CHOICES, required=True, label='Availability')

    # Enforce year format (YYYY) via integer constraints
    published_year = forms.IntegerField(
        min_value=1000,
        max_value=datetime.date.today().year,
        label='Published Year',
        widget=forms.NumberInput(attrs={'placeholder': 'YYYY'})
    )

    class Meta:
        model = Book
        fields = ['title', 'description', 'published_year', 'cover_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        # Allow passing initial related names via kwargs
        related_initial = kwargs.pop('related_initial', None)
        super().__init__(*args, **kwargs)
        # Update genre queryset at init in case genres are added later
        self.fields['genre'].queryset = Genre.objects.all()
        if related_initial:
            self.fields['author_name'].initial = related_initial.get('author')
            # related_initial['genre'] may be an id or Genre instance
            if related_initial.get('genre'):
                self.fields['genre'].initial = related_initial.get('genre')
            self.fields['library_name'].initial = related_initial.get('library')
            self.fields['availability_status'].initial = related_initial.get('availability')
