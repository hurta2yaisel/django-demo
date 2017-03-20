from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .views import home, add_contact, edit_contact, delete_contact, list_contact, export_contact, \
    add_group, edit_group, delete_group, list_group, login, register, logout

urlpatterns = [
    url(r'^$', home, name='home', ),
    url(r'^login/$', login, name='login', ),
    url(r'^register/$', register, name='register', ),
    url(r'^logout/$', logout, name='logout', ),
    url(r'^contact/$', list_contact, name='list_contact'),
    url(r'^contact/export/$', export_contact, name='export_contact'),
    url(r'^contact/new/$', add_contact, name='add_contact'),
    url(r'^contact/edit/(?P<id>\d+)$', edit_contact, name='edit_contact'),
    url(r'^contact/delete/(?P<id>\d+)$', delete_contact, name='delete_contact'),

    url(r'^group/$', list_group, name='list_group'),
    url(r'^group/new/$', add_group, name='add_group'),
    url(r'^group/edit/(?P<id>\d+)$', edit_group, name='edit_group'),
    url(r'^group/delete/(?P<id>\d+)$', delete_group, name='delete_group'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
