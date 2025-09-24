from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from catalog.models import *
from . forms import RenewBookForm

import datetime

# Create your views here.
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        # create a form instance and populate it with date from the request (binding)
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('borrowed-books'))
    else:
        propoed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(initial={'renewal_date':propoed_renewal_date})

    context = {
        'form' : form,
        'book_instance' : book_instance,
    }

    return render(request, "admin/book_renew_librarian.html" ,context)


class BorrowedBooksView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ("can_mark_returned",)
    permission_denied_message = "You are not admin "
    model = BookInstance
    template_name = "bookInstance/librarian/borrowed_books.html"
    paginated_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )
    
class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']
    template_name = "book/librarian/book_form.html"
    permission_required = 'catalog.add_book'


class BookInstanceCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):
    model = BookInstance
    fields = ['book','imprint','status']
    template_name = "bookInstance/librarian/bookinstance_form.html"
    initial = {
        'status' : 'a',
    }
    permission_required = 'catalog.add_bookinstance'


class BookInstanceUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
    model = BookInstance
    fields = ['due_back']
    permission_required = 'catalog.change_bookinstance'
    template_name = "bookInstance/librarian/bookinstance_form.html"
    success_url = reverse_lazy('borrowed-books')
    initial = {
        'due_back' : datetime.date.today() + datetime.timedelta(weeks=3)
    }


class BookInstanceDelete(PermissionRequiredMixin, generic.edit.DeleteView):
    model = BookInstance
    success_url = reverse_lazy('borrowed-books')
    permission_required = 'catalog.delete_bookinstance'
    template_name = "bookInstance/librarian/bookinstance_confirm_delete.html"
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('bookinstance-delete', kwargs={'pk' : self.object.pk})
            )

    