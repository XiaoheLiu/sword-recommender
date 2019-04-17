from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Review, Sword


class ReviewListView(ListView):
    model = Review
    context_object_name = 'review_list'
    ordering = ['-date_created']


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
        return context

    def form_valid(self, form):
        self.sword = get_object_or_404(Sword, pk=self.kwargs['sword_id'])
        form.instance.author = self.request.user
        form.instance.sword = self.sword
        return super().form_valid(form)


class SwordListView(ListView):
    model = Sword
    context_object_name = 'sword_list'
    ordering = ['sword_type']


class SwordDetailView(DetailView):
    model = Sword
    context_object_name = 'sword'
