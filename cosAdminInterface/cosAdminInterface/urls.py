from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'adminInterface.views.home', name='home'),
    url(r'^register/$', 'adminInterface.views.register', name='register'),
    url(r'^login/$', 'adminInterface.views.login', name='login'),
    url(r'^logout/$', 'adminInterface.views.logout', name='logout'),
    url(r'^users/$', 'adminInterface.views.users', name='users'),
    url(r'^prereg/$', 'adminInterface.views.prereg', name='prereg'),
    url(r'^prereg-form/(?P<draft_pk>[0-9a-z]+)/$', 'adminInterface.views.prereg_form', name='prereg_form'),
    url(r'^approve-draft/(?P<draft_pk>[0-9a-z]+)/$', 'adminInterface.views.approve_draft', name='approve_draft'),
    url(r'^reject-draft/(?P<draft_pk>[0-9a-z]+)/$', 'adminInterface.views.reject_draft', name='reject_draft'),
    url(r'^update-draft/(?P<draft_pk>[0-9a-z]+)/$', 'adminInterface.views.update_draft', name='update_draft'),
    url(r'^get-drafts/$', 'adminInterface.views.get_drafts', name='get_drafts'),
    url(r'^get-schemas/$', 'adminInterface.views.get_schemas', name='get_schemas'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'adminInterface.views.password_reset_confirm_custom', name='password_reset_confirm'),
    url(r'^reset/done/$', 'adminInterface.views.password_reset_done',
        name='password_reset_complete'),
    url('^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
