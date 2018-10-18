from django.urls import path

from . import views

urlpatterns = [
    # ex: /keiry/
    path('', views.index, name='index'),

    # ex: /keiry/journal/20180701/20190630/
    path('journal/<str:rec_date_fm>/<str:rec_date_to>/', views.journal, name='journal'),

    # ex: /keiry/journal/input/20180918/1
    path('journal/input/<str:rec_date>/<int:seq>', views.JournalView.as_view(), name='journal_detail'),
    path('journal/input/', views.JournalView.as_view(), name='journal_input'),

    # ex: /keiry/items
    path('items/', views.items, name='items'),

    # ex: /keiry/gcitems
    path('gcitems/', views.gcitems, name='gcitems'),

]
