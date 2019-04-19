from django.urls import path
from .views import ReviewListView, ReviewDetailView, ReviewCreateView, SwordListView, SwordDetailView, UserReviewListView

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('review/<int:pk>', ReviewDetailView.as_view(), name='review_detail'),
    path('sword', SwordListView.as_view(), name='sword_list'),
    path('sword/<int:pk>', SwordDetailView.as_view(), name='sword_detail'),
    path('sword/<int:sword_id>/new/',
         ReviewCreateView.as_view(), name='new_review'),
    path('review/user/<str:username>',
         UserReviewListView.as_view(), name='user_reviews'),
]
