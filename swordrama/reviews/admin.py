from django.contrib import admin

from .models import Sword, Review


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('sword', 'rating', 'author', 'comment', 'date_created')
    list_filter = ['date_created', 'author']
    search_fields = ['comment']


class SwordAdmin(admin.ModelAdmin):
    model = Sword
    list_display = ('name', 'sword_type', 'manufacturer', 'weight')
    list_filter = ['sword_type', 'manufacturer']
    search_fields = ['name']


admin.site.register(Sword, SwordAdmin)
admin.site.register(Review, ReviewAdmin)
