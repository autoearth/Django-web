from django.contrib import admin
from .models import *


admin.site.site_header = 'Sukoi Sushi Shop Admin'

admin.site.index_title = 'Main admin'

admin.site.site_title = 'Sukoi Sushi Shop Backend'

class AllproductAdmin(admin.ModelAdmin):
    list_display= ['name', 'id', 'instock','price','quantity']
    list_editable = ['instock','price','quantity']

admin.site.register(AllProduct, AllproductAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'usertype']

admin.site.register(Profile, ProfileAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display= ['user','productname','price','quantity', 'total']

admin.site.register(Cart, CartAdmin)

class OrderListAdmin(admin.ModelAdmin):
    list_display = ['orderid', 'productname', 'total']

admin.site.register(OrderList, OrderListAdmin)

class OrderPendingAdmin(admin.ModelAdmin):
    list_display = ['orderid','user','name','tel','address','shipping','payment','other','trackingnumber']

admin.site.register(OrderPending, OrderPendingAdmin)