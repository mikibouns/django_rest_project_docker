import django_filters
from .models import Basket


class BasketFilter(django_filters.FilterSet):

    class Meta:
        model = Basket
        fields = ['id', 'user_id']