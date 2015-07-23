from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
	url(r'^$', 'adminInterface.views.home', name='home'),
	#url(r'^users/$', 'adminInterface.views.users', name='users'),
	url(r'^prereg/$', 'adminInterface.views.prereg', name='prereg'),
	url(r'^get-drafts/$', 'adminInterface.views.get_drafts', name='get_drafts'),
	#url(r'^analystics/$', 'adminInterface.views.analytics', name='analytics'),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
