from django.urls import path
from .views import ReviewListView, ReviewDetailView, ReviewCreateView, SwordListView, SwordDetailView, UserReviewListView, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>', ReviewDetailView.as_view(), name='review_detail'),
    path('swords', SwordListView.as_view(), name='sword_list'),
    path('swords/<int:pk>', SwordDetailView.as_view(), name='sword_detail'),
    path('swords/<int:sword_id>/add_review/',
         ReviewCreateView.as_view(), name='new_review'),
    path('reviews/user/<str:username>',
         UserReviewListView.as_view(), name='user_reviews'),
]
