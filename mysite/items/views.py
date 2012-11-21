from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from list.models import *


def index(request):
    list = Item.objects.all().order_by('-created')
    return render_to_response('item/index.html',{'list':list})

def item(request, id):
    try:
        i = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404
    return render_to_response('item/item.html', {'item':i})
