from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from reviews.models import Review, Sword
from random import sample


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Thank you for joining SwordRama, {username}! Please login now.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Sign Up'})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            message.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    context = {'user_form': user_form}
    return render(request, 'users/profile.html', context)


@login_required
def recommendation(request):
    user_reviews = Review.objects.filter(
        author=request.user).prefetch_related('sword')
    user_reviews_sword_ids = set(map(lambda x: x.sword.id, user_reviews))
    # sword_list = Sword.objects.exclude(id__in=user_reviews_sword_ids)
    id_list = Sword.objects.exclude(
        id__in=user_reviews_sword_ids).values_list('id', flat=True)
    random_id_list = sample(list(id_list), 10)
    sword_list = Sword.objects.filter(id__in=random_id_list)

    context = {'user': request.user, 'sword_list': sword_list}
    return render(request, 'users/recommendation.html', context)
