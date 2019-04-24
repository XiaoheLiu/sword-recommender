from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Review, Sword
from .recommendations import update_clusters


def home_view(request):
    review_list = [Review.objects.first(), Review.objects.last()]
    sword_count = Sword.objects.count()
    review_count = Review.objects.count()
    context = {
        'review_list': review_list,
        'sword_count': sword_count,
        'review_count': review_count,
    }
    return render(request, 'reviews/home.html', context)


class ReviewListView(ListView):
    model = Review
    context_object_name = 'review_list'
    ordering = ['-date_created']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Latest Reviews for Various HEMA Weapons'
        return context


class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['comment', 'rating']

    def get_context_data(self, **kwargs):
        self.sword = get_object_or_404(Sword, pk=self.kwargs['sword_id'])
        context = super().get_context_data(**kwargs)
        context['sword'] = self.sword
        context['title'] = 'Add Your Review'
        return context

    def form_valid(self, form):
        self.sword = get_object_or_404(Sword, pk=self.kwargs['sword_id'])
        form.instance.author = self.request.user
        form.instance.sword = self.sword
        update_clusters()
        return super().form_valid(form)


class SwordListView(ListView):
    model = Sword
    context_object_name = 'sword_list'
    ordering = ['sword_type']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'View All Swords'
        return context


class SwordDetailView(DetailView):
    model = Sword
    context_object_name = 'sword'


class UserReviewListView(ListView):
    model = Review
    template_name = 'reviews/user_reviews.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(author=user).order_by('-date_created')
