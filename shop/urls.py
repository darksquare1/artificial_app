from django.urls import path

from shop.views import GoodsListView

urlpatterns = [
    path('goods/', GoodsListView.as_view(), name='list-goods')
]
