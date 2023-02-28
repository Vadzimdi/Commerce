from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid)




