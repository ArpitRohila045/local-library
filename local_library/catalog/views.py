from django.shortcuts import render
from . models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from . forms import RenewBookForm
import datetime

def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_avilable = BookInstance.objects.filter(status='a').count()

    num_authors = Author.objects.count()

    genrs = Genre.objects.all()
    counter = {genre.name: Book.objects.filter(id=genre.id).count() for genre in genrs}

    # print(counter)
    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_avilable' : num_instances_avilable,
        'num_authors' : num_authors,
        'genrs' : genrs,
        'counter' : counter,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    login_url = "/login/"
    redirect_field_name = "request.path"

    model = Book
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "This is just some data"
        return context


class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 3
    

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3


class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    # permission_required = ("catalog.can_mark_returned", "catalog.change_book") 
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginated_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
