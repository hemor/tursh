from django.conf.urls import url
from . import views


app_name = 'shortener'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^shorten_url/$', views.shorten_url, name='shorten_url'),
    url(r'^process_widget/$', views.process_widget, name='process_widget'),
    url(r'^widget/$', views.widget, name="widget"),
    url(r'^(?P<short_url>[0-9A-Za-z]{6})/$', views.redirect_original, name='redirect_original'),
]