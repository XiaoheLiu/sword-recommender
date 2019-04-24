from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.models import User
from random import sample
from reviews.models import Review, Sword, Cluster
from reviews.recommendations import update_clusters


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
    # 1. Get current user's reviews
    user_reviews = Review.objects.filter(
        author=request.user).prefetch_related('sword')
    user_reviews_sword_ids = set(map(lambda x: x.sword.id, user_reviews))

    # 2. Get this user's cluster name
    try:
        user_cluster_name = User.objects.get(
            username=request.user.username).cluster_set.first().name
    except:
        # If this user does not belong to any cluster, update the clusters.
        update_clusters()
        user_cluster_name = User.objects.get(
            username=request.user.username).cluster_set.first().name

    # 3. Get other members in this cluster
    other_cluster_members = Cluster.objects.get(
        name=user_cluster_name).users.exclude(username=request.user.username).all()

    # 4. Get reviews by other members, excluding swords reviewed by the current user
    other_members_reviews = Review.objects.filter(
        author__in=other_cluster_members).exclude(sword__id__in=user_reviews_sword_ids)
    other_members_reviews_sword_ids = set(
        map(lambda x: x.sword.id, other_members_reviews))

    # 5. Create a sword list including the above sword ids, order by rating
    sword_list = sorted(
        list(Sword.objects.filter(id__in=other_members_reviews_sword_ids)),
        key=Sword.average_rating,
        reverse=True
    )

    # 6. If there are less than 10 recommendations, fill in the rest slots with random picked swords that have not been rated by the user
    if len(sword_list) < 10:
        num_needed = 10-len(sword_list)
        rest_sword_ids = Sword.objects.exclude(
            id__in=user_reviews_sword_ids).exclude(id__in=other_members_reviews_sword_ids).values_list('id', flat=True)
        random_sword_id_list = sample(list(rest_sword_ids), num_needed)
        sword_list += Sword.objects.filter(id__in=random_sword_id_list)

    context = {'user': request.user, 'sword_list': sword_list}
    return render(request, 'users/recommendation.html', context)
