from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Comments, Category, Product, OurTeam, Status, Cart, ProductsProducts, ProductsUsers


admin.site.register([ProductsProducts, ProductsUsers])


@admin.register(Status)
class StatusAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'created_date', 'last_update')
    list_display_links = ('id', 'name', 'created_date', 'last_update')
    search_fields = ('id', 'name', 'created_date', 'last_update')
    list_filter = ('id', 'name')
    date_hierarchy = 'created_date'
    ordering = ('id', )


@admin.register(OurTeam)
class OurTeamAdmin(ImportExportModelAdmin):
    list_display = ('id', 'created_date', 'last_update')
    list_display_links = ('id', 'created_date', 'last_update')
    search_fields = ('id', 'status__name', 'employee__username')
    list_filter = ('id', )
    ordering = ('id', )


@admin.register(Comments)
class CommentsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'text_10', 'created_date', 'last_update')
    list_display_links = ('id', 'created_date', 'last_update')
    search_fields = ('id', "customer__username", 'text', 'created_date', 'last_update')
    list_filter = ('id', 'customer__username')
    date_hierarchy = 'created_date'
    ordering = ('id', 'created_date')

    def text_10(self, obj):
        return obj.text[: 10]


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'created_date', 'last_update')
    list_display_links = ('id', 'title', 'created_date', 'last_update')
    search_fields = ('id', 'title')
    list_filter = ('id', 'title')
    date_hierarchy = 'created_date'
    ordering = ('id', 'created_date')


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'price', 'price_type', 'rating', 'created_date')
    list_display_links = ('id', 'title', 'price', 'price_type', 'rating', 'created_date')
    search_fields = ('id', 'title', 'rating', 'price', 'price_type')
    list_filter = ('title', 'price')
    ordering = ('id', 'title')


@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product_number', 'payment_status', 'created_date', 'last_update')
    list_display_links = ('id', 'product_number', 'payment_status', 'created_date', 'last_update')
    search_fields = ('id', 'product_number', )
    list_filter = ('id',)
    ordering = ('id', 'product_number')
