from django.contrib import admin

from shop.models import Goods


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    pass


