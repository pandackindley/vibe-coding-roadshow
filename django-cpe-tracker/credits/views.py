from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.contrib.auth.models import User


from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

def hello_world(request):
	return render(request, 'credits/hello_world.html')

# View to select user
def select_user(request):
	users = User.objects.all()
	return render(request, 'credits/select_user.html', {'users': users})

# View to handle login for a selected user
def login_user(request, username):
	error = None
	if request.method == 'POST':
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('landing'))
		else:
			error = 'Invalid password. Please try again.'
	return render(request, 'credits/login_user.html', {'username': username, 'error': error})


# Landing page after login
from django.contrib.auth.decorators import login_required
from .forms import CPEExperienceForm
from .models import CPEExperience

@login_required
def landing(request):
	experiences = CPEExperience.objects.filter(user=request.user).order_by('-date_accomplished')
	return render(request, 'credits/landing.html', {'experiences': experiences})

@login_required
def add_cpe_experience(request):
	if request.method == 'POST':
		form = CPEExperienceForm(request.POST)
		if form.is_valid():
			cpe = form.save(commit=False)
			cpe.user = request.user
			cpe.save()
			return HttpResponseRedirect(reverse('landing'))
	else:
		form = CPEExperienceForm()
	return render(request, 'credits/add_cpe_experience.html', {'form': form})


@login_required
def edit_cpe_experience(request, pk):
	cpe = get_object_or_404(CPEExperience, pk=pk, user=request.user)
	if request.method == 'POST':
		form = CPEExperienceForm(request.POST, instance=cpe)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('landing'))
	else:
		form = CPEExperienceForm(instance=cpe)
	return render(request, 'credits/add_cpe_experience.html', {'form': form, 'edit': True})

# Create your views here.
