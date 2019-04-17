from django.contrib import admin

from .models import Sword, Review


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('sword', 'rating', 'author', 'comment', 'date_created')
    list_filter = ['date_created', 'author']
    search_fields = ['comment']


admin.site.register(Sword)
admin.site.register(Review, ReviewAdmin)
