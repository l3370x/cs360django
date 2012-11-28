from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect


from dog.models import *
from person.models import *
from orders.models import *

@login_required
def new(request):
    theDog = Dog.objects.get(id=request.session['dog'])
    if request.method == 'GET':
        form = OrdersForm()
        return render_to_response('orders/new.html', {'form':form,'dog':theDog},
                                  context_instance=RequestContext(request))
    if request.method =='POST':
        form = OrdersForm(request.POST)
        if not form.is_valid():
            return render_to_response('orders/new.html', {'form':form,'error':True},
                                      context_instance=RequestContext(request))

        i = Orders()
        i.credit_card = form.cleaned_data['credit_card']
        i.card_security_code = form.cleaned_data['card_security_code']
        i.expiry_date = form.cleaned_data['expiry_date']
        fosterPerson = Person.objects.get(user=request.user.id)
        theDog = Dog.objects.get(id=request.session['dog'])
        i.person_id = fosterPerson
        i.dog_id = theDog
        i.save()
        adopt(i)
        return render_to_response('orders/thanks.html')

def adopt(orders):
    theDog = Dog.objects.get(id=orders.dog_id.id)
    thePerson = Person.objects.get(id=orders.person_id.id)
    print "do the following:"
    print theDog
    print thePerson
    print theDog.foster_id
    theDog.foster_id = thePerson
    print theDog
    print thePerson
    print theDog.foster_id
    theDog.save()


