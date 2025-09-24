from django.urls import path
from . import views

urlpatterns = [
    # path("adduser/", ),
    # path("deleteuser/",),
    # path("addbookinstance/"),
    # path("addauthor/"),

    path("addbook/", views.BookCreate.as_view(), name="create-book"),
    path('borrowed/', views.BorrowedBooksView.as_view(), name='borrowed-books'),

    # book instance
    path('bookinstancecreate/', views.BookInstanceCreate.as_view(), name='bookinstance-create'),
    path('book/<uuid:pk>/renew', views.BookInstanceUpdate.as_view(), name='bookinstance-update'),
    path('book/<uuid:pk>/delete', views.BookInstanceDelete.as_view(), name='bookinstance-delete'),
]