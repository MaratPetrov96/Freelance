from django.contrib import admin
from .models import *

#admin.site.register(SiteUser)
admin.site.register(Category)

class Seller(admin.TabularInline):
    model = SiteUser.categories.through

@admin.register(SiteUser)
class OfferAdmin(admin.ModelAdmin):
    inlines = (Seller,)
    exclude = ('categories',)

admin.site.register(Order)
admin.site.register(Offer)
admin.site.register(PortProject)
admin.site.register(View)
admin.site.register(Message)
# Register your models here.
