from django.contrib import admin
from .models import Address, EventCategory, EventDetails, Cart, Order

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('Name', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('categorytitle', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('categorytitle', 'description')
    prepopulated_fields = {"slug": ("categorytitle", )}


class EventDetailsAdmin(admin.ModelAdmin):
    list_display = ('Eventtitle', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('Eventtitle', 'category')
    prepopulated_fields = {"slug": ("Eventtitle", )}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')


admin.site.register(Address, AddressAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(EventDetails, EventDetailsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)