from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Review, Sword
from .recommendations import update_clusters
from .filters import SwordFilter


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


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['comment', 'rating']
    template_name = 'reviews/update_review.html'

    def get_context_data(self, **kwargs):
        review = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Review'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("sword_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(
            self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class SwordListView(FilteredListView):
    filterset_class = SwordFilter
    model = Sword
    context_object_name = 'sword_list'
    paginate_by = 20


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
