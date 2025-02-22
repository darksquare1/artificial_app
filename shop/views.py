from django.db.models import Q
from rest_framework.generics import ListAPIView

from shop.models import Goods
from shop.serializers import GoodsSerializer


class GoodsListView(ListAPIView):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        queryset = Goods.objects.all()
        conditions = Q()
        name = self.request.query_params.get('name')
        tag = self.request.query_params.get('tag')
        description = self.request.query_params.get('description')
        if name:
            conditions |= Q(name__icontains=name)
        if tag:
            conditions |= Q(tags__name__icontains=tag)
        if description:
            conditions |= Q(description__icontains=description)
        if conditions:
            return queryset.filter(conditions)
        return queryset
