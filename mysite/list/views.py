from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from list.models import *

@login_required
def index(request):
    list = Item.objects.filter(user=request.user.id).order_by('-created')
    return render_to_response('item/index.html',
                              {'list':list,
                               'today':get_today(request)})

@login_required
def item(request, id):
    try:
        i = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404
    if i.user_id != request.user.id:
        raise Http404
    return render_to_response('item/item.html', {'item':i})

@login_required
def add(request):
    if request.method == 'GET':
        form = ItemForm()
        return render_to_response('item/add.html', {'form':form},
                                  context_instance=RequestContext(request))
    if request.method =='POST':
        form = ItemForm(request.POST)
        if not form.is_valid():
            return render_to_response('item/add.html', {'form':form},
                                      context_instance=RequestContext(request))

        i = Item()
        i.user = request.user
        i.text = form.cleaned_data['text']
        i.save()
        return HttpResponseRedirect(reverse('list.views.index'))

@login_required
def edit(request, id):
    try:
        i = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404
    if i.user_id != request.user.id:
        raise Http404
    if request.method == 'GET':
        form = ItemForm(instance=i)
        return render_to_response('item/edit.html', {'form':form,
                                                     'item':i},
                                  context_instance=RequestContext(request))
    if request.method =='POST':
        form = ItemForm(request.POST)
        if not form.is_valid():
            return render_to_response('item/edit.html', {'form':form,
                                                         'item':i},
                                      context_instance=RequestContext(request))

        i.text = form.cleaned_data['text']
        i.save()
        return HttpResponseRedirect(reverse('list.views.index'))

@login_required
def delete(request, id):
    try:
        i = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404
    if i.user_id != request.user.id:
        raise Http404
    remove_today(request, i)
    i.delete()
    return HttpResponseRedirect(reverse('list.views.index'))


@login_required
def today(request, id):
    try:
        i = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404
    if i.user_id != request.user.id:
        raise Http404
    today = add_today(request, i)
    return HttpResponseRedirect(reverse('list.views.index'))

@login_required
def later(request, id):
    try:
        i = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404
    if i.user_id != request.user.id:
        raise Http404
    today = remove_today(request, i)
    return HttpResponseRedirect(reverse('list.views.index'))


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        request.session['next'] = request.GET['next']
        return render_to_response('auth/login.html', {'form':form,
                                                      'login':True},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render_to_response('auth/login.html', {'form':form},
                                  context_instance=RequestContext(request))

        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render_to_response('auth/login.html',
                                      {'form':form,
                                       'login':True,
                                       'error': 'Invalid username or password'},
                                      context_instance=RequestContext(request))
        django.contrib.auth.login(request,user)
        return HttpResponseRedirect(request.session['next'])

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('list.views.index'))

def create(request):
    if request.method == 'GET':
        form = UserForm()
        return render_to_response('auth/create.html', {'form':form},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = UserForm(request.POST)
        if not form.is_valid():
            return render_to_response('auth/create.html', {'form':form},
                                  context_instance=RequestContext(request))

        try:
            u = User.objects.get(username=request.POST['username'])
            return render_to_response('auth/create.html',
                                      {'form':form,
                                       'error':'Username already taken'},
                                  context_instance=RequestContext(request))
        except User.DoesNotExist:
            pass

        if request.POST['password'] != request.POST['confirm']:
            return render_to_response('auth/create.html',
                                      {'form':form,
                                       'error':'Passwords must match'},
                                  context_instance=RequestContext(request))

        user = User.objects.create_user(request.POST['username'],
                                        request.POST['email'],
                                        request.POST['password'])
        user.save()
        return HttpResponseRedirect(reverse('list.views.index'))

def get_today(request):
    if not request.session.has_key('today'):
        request.session['today'] = []
    return request.session['today']

def add_today(request, item):
    l = get_today(request)
    if item not in l:
        l.append(item)
        request.session.modified = True
    return l

def remove_today(request, item):
    l = get_today(request)
    if item in l:
        l.remove(item)
        request.session.modified = True
    return l
