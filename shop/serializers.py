from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from shop.models import Goods


class GoodsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Goods
        fields = '__all__'
