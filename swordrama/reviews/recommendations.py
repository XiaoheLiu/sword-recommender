from django.contrib.auth.models import User
from .models import Review, Sword, Cluster
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np


def update_clusters(is_new_user):
    num_reviews = Review.objects.count()
    update_step = 10
    # Recluster users when every <update_step> reviews are added or when a new user is created
    if num_reviews % update_step == 0 or is_new_user:
        # Retrieve user reviews data
        all_users = User.objects.only("username")
        all_reviewed_sword_ids = set(
            map(lambda x: x.sword.id, Review.objects.only("sword")))
        num_users = len(all_users)

        # Create a sparse matrix for ratings
        ratings_m = dok_matrix(
            (num_users, max(all_reviewed_sword_ids)+1), dtype=np.float32)

        # Each user is a row, columns has their ratings
        for i in range(num_users):
            user_reviews = Review.objects.filter(author=all_users[i])
            for user_review in user_reviews:
                ratings_m[i, user_review.sword.id] = user_review.rating

        # Perform kmeans clustering
        k = int(num_users/10) + 2  # at least 2 clusters
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())

        # Re-cluster all users
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values():
            cluster.save()
        for i, cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(
                User.objects.get(username=all_users[i].username))
