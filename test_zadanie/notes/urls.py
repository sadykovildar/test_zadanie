from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^note/(?P<note_id>[^/]+)/$', views.one_note, name='one_note'),
    url(r'^note/edit/(?P<note_id>[^/]+)/$', views.edit_note, name='edit_note'),
    url(r'^note/delete/(?P<note_id>[^/]+)/$', views.delete_note, name='delete_note'),
    url(r'^del/$', views.del_note_on_index, name='del_note_on_index'),
    url(r'^setChosen/$', views.set_chosen, name='set_chosen'),
    url(r'^notes/save_edited_note/(?P<note_id>[^/]+)/$', views.save_edited_notes, name='save_edited_notes'),
    url(r'^notes/newnote/$', views.newnote, name='newnote'),
    url(r'^sort/$', views.sort_ajax, name='sort_ajax'),
    url(r'^search/$', views.search_ajax, name='search_ajax'),
    url(r'^note/open_note/(?P<note_id>[^/]+)/$', views.open_note, name='open_note'),
    url(r'^note/close_note/(?P<note_id>[^/]+)/$', views.close_note, name='close_note'),
    url(r'^$', views.index, name='index'),

]
