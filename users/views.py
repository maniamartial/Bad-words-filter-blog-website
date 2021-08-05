from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.


'''def login(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)
'''


def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    context = {'form': form}
    return render(request, 'users/register.html', context)


# def logout(request):
 #   pass
@login_required
def profile(request):
    return render(request, 'users/profile.html')
