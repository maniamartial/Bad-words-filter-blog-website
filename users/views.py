from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ProfileUpdateForm, UserRegisterForm, User_Update_Form
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
    if request.method == 'POST':

        u_form = User_Update_Form(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES,  instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated successfully!')
            return redirect('profile')
    else:
        u_form = User_Update_Form(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
