from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.http import HttpResponseRedirect
from django.shortcuts import render



from dog.models import *
from person.models import *
from qualities.models import *
from pictures.models import *
from breed.models import *


def home(request):
    doglist = Dog.objects.all().order_by('-date_added')
    if request.user.is_authenticated():
        if request.user.username == 'aaron':
            logout(request)
            return render_to_response('home.html',
                              {'doglist':doglist,'newbie':True})
        return index(request)
    return render_to_response('home.html',
                              {'doglist':doglist,'newbie':True})



@login_required
def index(request,who='me'):
    doglist = Dog.objects.filter(foster_id=Person.objects.get(user=request.user.id)).order_by('-date_added')
    if who == 'all':
        doglist = Dog.objects.all().order_by('-date_added')
    if who == 'find':
        doglist = Dog.objects.filter(up_for_adoption=True).order_by('-date_added')
    piclist = []
    for dog in doglist:
        pics = dict({'theDog':dog,'thePics':Picture.objects.filter(dog_id=dog.id)})
        piclist.append(pics)
    print piclist
    return render_to_response('dog/index.html',
                              {'doglist':doglist,'who':who,'piclist':piclist})

@login_required
def all(request):
    return index(request,'all')

@login_required
def find(request):
    return index(request,'find')

@login_required
def dog(request, id):
    try:
        i = Dog.objects.get(pk=id)
    except Dog.DoesNotExist:
        raise Http404
    request.session["dog"] = id
    myBreeds = Breed.objects.filter(dog_id = i.id)
    myQualities = Quality.objects.filter(dog_id = i.id)
    myPictures = Picture.objects.filter(dog_id = i.id)
    isOwner = request.user.username == i.foster_id.user.username
    return render_to_response('dog/dog.html', {'dog':i,'myBreeds':myBreeds,'isOwner':isOwner
                                               ,'myQualities':myQualities,'myPictures':myPictures})


from sorl.thumbnail import get_thumbnail
from PIL import Image

def validateImage(image,request):
    for img in request.FILES:
        print 'below is the image'
        print img
#    im = get_thumbnail(my_file, '100x100', crop='center', quality=99)
    return image.is_valid()

@login_required
def submit_dog(request):
    if request.POST:
        form = UserSubmittedDogForm(request.POST)
        breed_formset = BreedFormSet(request.POST)
        quality_formset = QualityFormSet(request.POST)
        picture_formset = PictureFormSet(request.POST)
        if form.is_valid():
            dog = form.save(commit=False)
            breed_formset = BreedFormSet(request.POST, instance=dog)
            quality_formset = QualityFormSet(request.POST, instance = dog)
            picture_formset = PictureFormSet(request.POST, request.FILES, instance = dog)
            if breed_formset.is_valid() and quality_formset.is_valid() and validateImage(picture_formset,request):
                fosterPerson = Person.objects.get(user=request.user.id)
                dog.foster_id = fosterPerson
                dog.save()
                breed_formset.save()       
                quality_formset.save() 
                picture_formset.save()         
            return index(request)
            
    else:
        form = UserSubmittedDogForm()
        breed_formset = BreedFormSet(instance=Dog())
        quality_formset = QualityFormSet(instance=Dog())
        picture_formset = PictureFormSet(instance=Dog())
    return render_to_response("dog/add.html", {
        "form": form,
        "breed_formset": breed_formset,
        "quality_formset": quality_formset,
        "picture_formset": picture_formset,
    }, context_instance=RequestContext(request))
#

@login_required
def person(request, id):
    try:
        i = Person.objects.get(pk=id)
    except Person.DoesNotExist:
        raise Http404
    return render_to_response('person/person.html', {'person':i})

BreedFormSet2 = inlineformset_factory(Dog, 
    Breed, 
    can_delete=False)

@login_required
def edit(request, id):
    try:
        i = Dog.objects.get(pk=id)
    except Dog.DoesNotExist:
        raise Http404
    if i.foster_id.id != Person.objects.get(user=request.user.id).id:
        raise Http404
#
    if request.POST:
        form = UserSubmittedDogForm(request.POST, instance = i)
        breed_formset = BreedFormSet(request.POST, instance = i)
        quality_formset = QualityFormSet(request.POST, instance = i)
        picture_formset = PictureFormSet(request.POST, request.FILES, instance = i)
        if form.is_valid() and breed_formset.is_valid() and quality_formset.is_valid() and picture_formset.is_valid():
            form.save()
            breed_formset.save()    
            quality_formset.save()
            picture_formset.save()            
            return dog(request,id)
    else:
        form = UserSubmittedDogForm(instance=i)
        breed_formset = BreedFormSet(instance=i)
        quality_formset = QualityFormSet(instance=i)
        picture_formset = PictureFormSet(instance=i)
    return render_to_response("dog/edit.html", {
        "form": form,
        "breed_formset": breed_formset,
        "quality_formset": quality_formset,
        "picture_formset": picture_formset,
    }, context_instance=RequestContext(request))
#
    

@login_required
def delete(request, id):
    try:
        i = Dog.objects.get(pk=id)
    except Dog.DoesNotExist:
        raise Http404
    if i.foster_id.id != Person.objects.get(user=request.user.id).id:
        raise Http404
    i.delete()
    return index(request)


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        request.session['next'] = request.GET['next']
        return render_to_response('auth/login.html', {'form':form,'create':True,
                                                      'login':True},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render_to_response('auth/login.html', {'form':form,'create':True},
                                  context_instance=RequestContext(request))

        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render_to_response('auth/login.html',
                                      {'form':form,'create':True,
                                       'error': 'Invalid username or password'},
                                      context_instance=RequestContext(request))
        django.contrib.auth.login(request,user)
        return HttpResponseRedirect(request.session['next'])

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('person.views.index'))

def loginDirect(request,username,password):
    print "username"
    print username
    print password
    print "password"
    user = authenticate(username=username,
                            password=password)
    if user is None:
        form = LoginForm()
        return render_to_response('auth/login.html',
                                  {'form':form,'create':True,
                                   'error': 'Invalid username or password'},
                                  context_instance=RequestContext(request))
    django.contrib.auth.login(request,user)
    return HttpResponseRedirect(request.session['next'])

def create(request):
    if request.method == 'GET':
        form = UserForm()
        return render_to_response('auth/create.html', {'form':form,'create':True},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = UserForm(request.POST)
        if not form.is_valid():
            return render_to_response('auth/create.html', {'form':form,'create':True},
                                  context_instance=RequestContext(request))

        try:
            u = User.objects.get(username=request.POST['username'])
            return render_to_response('auth/create.html',
                                      {'form':form,
                                       'error':'Username already taken','create':True},
                                  context_instance=RequestContext(request))
        except User.DoesNotExist:
            pass

        if request.POST['password'] != request.POST['confirm']:
            return render_to_response('auth/create.html',
                                      {'form':form,
                                       'error':'Passwords must match','create':True},
                                  context_instance=RequestContext(request))

        userO = User.objects.create_user(request.POST['username'],
                                        request.POST['email'],
                                        request.POST['password'])
        userO.save()
        person = Person.objects.create(user=userO,first_name=request.POST['first_name'],
                                            last_name=request.POST['last_name'],
                                            address=request.POST['address'],
                                            city=request.POST['city'],
                                            zipcode=request.POST['zipcode'],
                                            state=request.POST['state'],
                                            email=request.POST['email'])

        
        request.session["next"] = "/person/"
        return loginDirect(request,request.POST['username'],request.POST['password'])
