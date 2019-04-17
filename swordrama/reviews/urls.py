from django.urls import path
from .views import ReviewListView, ReviewDetailView, ReviewCreateView, SwordListView, SwordDetailView

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('review/<int:pk>', ReviewDetailView.as_view(), name='review_detail'),
    path('sword', SwordListView.as_view(), name='sword_list'),
    path('sword/<int:pk>', SwordDetailView.as_view(), name='sword_detail'),
    path('sword/<int:sword_id>/new/',
         ReviewCreateView.as_view(), name='new_review'),

]

# urlpatterns = [
#     path('', PostListView.as_view(), name='blog-home'),
#     path('post/user/<str:username>', UserPostListView.as_view(), name='user-posts'),
#     path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
#     path('post/new/', PostCreateView.as_view(), name='post-create'),
#     path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
#     path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
#     path('about/', views.about, name='blog-about'),
# ]
