from django.shortcuts import render

# Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages


def loginview(request):

    if request.method == 'GET':
        c = csrf(request)
        if request.GET.get('next'):
            c.update({'next': request.GET['next']})
        return render_to_response('registration/login.html', RequestContext(request, c))

    elif request.method == 'POST':
        old_user = request.user or None

        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)

            next_page = request.POST.get('next', None)

            # If the user was already logged-in before we ignore the ?next
            # parameter, this avoids a loop of login prompts when the user does
            # not have the permission to see the page in ?next
            if old_user == user or not next_page:
                # Redirect chefs to meals page
                if bool(request.user.groups.filter(name="Chef")) and request.user.has_perm('meals.view_meal'):
                    next_page = reverse('meals-index')
                else:
                    next_page = reverse('accounts-dashboard')

            return HttpResponseRedirect(next_page)

        else:
            messages.error(request, 'Login failed. Please try again.')
            return redirect('accounts-login')