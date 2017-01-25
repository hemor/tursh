import string
import random
import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from .models import ShortUrl
from . import validators as va


PROTOCOLS = ['http', 'https', 'ftp', 'ftps']


#   TODO:2 - Add more comments to js and python files


@csrf_protect
def index(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'index.html', c)


def redirect_original(request, short_url):
    #   Redirect short url to it's full url
    try:
        url = ShortUrl.objects.get(short_url=short_url)
    except:
        return render(request, '404.html')

    url.increase_count()
    return redirect(url.full_url)


@csrf_protect
def shorten_url(request):
    #   Process creation of short url
    if request.is_ajax():
        if request.method == 'POST':
            full_url = request.POST.get('full_url', '')
            short_url = request.POST.get('short_url', '')
            response = {
                'error': {'short_url': '', 'full_url': ''},
                'data': {'short_url': '', 'full_url': ''}
            }
            error = False

            if not short_url:
                short_url = generate_short_url()
            if not va.valid_short_url(short_url):
                error = True
                response['error']['short_url'] = 'Enter a valid short url'
            if not va.unique_short_url(short_url):
                error = True
                response['error']['short_url'] = 'Short url already exists'

            #   If full_url doesn't start with http, https, ftp or ftps append http to it.
            #   Needed for the url validation to work.
            if (not full_url.split('://')[0] in PROTOCOLS):
                full_url = '%s://%s'%(PROTOCOLS[0], full_url)
            if not va.valid_url(full_url):
                error = True
                response['error']['full_url'] = 'Enter a valid url'

            if not error:
                if settings.DEBUG:
                    host = get_current_site(request)
                else:
                    host = 'www.tursh.net'
                try:
                    new_url = ShortUrl.objects.get(full_url=full_url)   #   If full_url already exist
                    response['data']['short_url'] = '%s/%s'%(host, new_url.short_url)
                    response['data']['full_url'] = new_url.full_url
                except ShortUrl.DoesNotExist:   #   Create a new one if the full_url doesnt exist already
                    new_url = ShortUrl.objects.create(full_url=full_url, short_url=short_url)
                    new_url.save()
                    response['data']['short_url'] = '%s/%s'%(host, new_url.short_url)
                    response['data']['full_url'] = new_url.full_url
            return HttpResponse(json.dumps(response), content_type='application/json')
    return render(request, '400.html')


def generate_short_url(size=6):
    #   Generate random chars of length size from [a-zA-Z0-9]
    options = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(options) for x in range(size))
        try:
            url = ShortUrl.objects.get(short_url=short_url)
        except ShortUrl.DoesNotExist:
            return short_url


def widget(request):
    if request.GET.get('callback', '') != '':   #   If callback is present display the widget form.
        data = {}
        html = ""
        if request.GET.get('widget_type', '') == 'short':
            html = "<div class='col-xs-offset-3 col-xs-6'><p style='color: red; font-weight: bold; visibility: hidden' \
            id='pFullUrlError'>full url error</p><div class='row' style='margin-bottom: 10px'><div class='col-xs-9'> \
            <input class='form-control input-md' type='text' name='full_url' id='widFullUrl' placeholder= \
            'Enter Full URL' maxlength='2000'/></div><div class='col-xs-3' id='btnDiv'><button class='form-control btn-primary' \
            type='button' id='widSubmitForm' onclick='post_url();'>Shrink</button></div></div></div>"

        elif request.GET.get('widget_type', '') == 'long':
            html = "<div class='col-xs-offset-3 col-xs-6'><p style='color: red; font-weight: bold; visibility: hidden' \
            id='pFullUrlError'>full url error</p><div class='row' style='margin-bottom: 10px'><div class='col-xs-9'> \
            <input class='form-control input-md' type='text' name='full_url' id='widFullUrl' placeholder='Enter Full URL' \
            maxlength='2000'/></div><div class='col-xs-3' id='btnDiv'><button class='form-control btn-primary' type='button' \
            id='widSubmitForm' onclick='post_url();'>Shrink</button></div></div><p style='color: red; font-weight: bold; visibility:\
            hidden' id='pShortUrlError'>short url error</p><div class='row'><div class='col-xs-9'><input type='text' \
            class='form-control input-md' name='short_url' placeholder='Enter short URL (OPTIONAL)' maxlength='6' \
            id='widShortUrl'/></div></div></div>"

        else:
            html = "Error"

        data.update({"html": html})
        return HttpResponse("%s(%s)"%(request.GET.get('callback'), json.dumps(data)))
    return redirect('/static/js/widget/widget.js')  #   Return the widget js instead.


def process_widget(request):
    #   Process submission from widget
    if request.GET.get('callback', '') != '':
        full_url = request.GET.get('full_url', '')
        short_url = request.GET.get('short_url', '')
        response = {
            'error': {'short_url': '', 'full_url': ''},
            'data': {'short_url': '', 'full_url': ''}
        }
        error = False

        if not short_url:
            short_url = generate_short_url()
        if not va.valid_short_url(short_url):
            error = True
            response['error']['short_url'] = 'Enter a valid short url'
        if not va.unique_short_url(short_url):
            error = True
            response['error']['short_url'] = 'Short url already exists'

        #   If full_url doesn't start with http, https. ftp or ftps append http to it.
        #   Needed for the url validation to work.
        if (not full_url.split('://')[0] in PROTOCOLS):
            full_url = '%s://%s'%(PROTOCOLS[0], full_url)
        if not va.valid_url(full_url):
            error = True
            response['error']['full_url'] = 'Enter a valid url'

        if not error:
            if settings.DEBUG:
                host = get_current_site(request)
            else:
                host = 'www.tursh.net'
            try:
                new_url = ShortUrl.objects.get(full_url=full_url)
                response['data']['short_url'] = '%s/%s'%(host, new_url.short_url)
                response['data']['full_url'] = new_url.full_url
            except ShortUrl.DoesNotExist:
                new_url = ShortUrl.objects.create(full_url=full_url, short_url=short_url)
                new_url.save()
                response['data']['short_url'] = '%s/%s'%(host, new_url.short_url)
                response['data']['full_url'] = new_url.full_url
        return HttpResponse("%s(%s)"%(request.GET.get('callback'), json.dumps(response)))
    return HttpResponse('Bad Request')


#   TODO:4 - shorten_url and process_widget views are similar and violate the DRY principle look for a way to combine them
