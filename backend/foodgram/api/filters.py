import django_filters

from recipes.models import Recipe


class FavoriteShoppingFilter(django_filters.FilterSet):
    is_favorited = django_filters.NumberFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = django_filters.CharFilter(method='filter_tags')
    author = django_filters.NumberFilter(
        method='filter_author'
    )

    def _filter(self, queryset, field, value, filtered):
        if value:
            return filtered
        return queryset

    def filter_is_favorited(self, queryset, field, value):
        user = self.request.user
        filtered = queryset.filter(favorite__user=user)
        return self._filter(queryset, field, value, filtered)

    def filter_is_in_shopping_cart(self, queryset, field, value):
        user = self.request.user
        filtered = queryset.filter(shopping__user=user)
        return self._filter(queryset, field, value, filtered)

    def filter_tags(self, queryset, field, value):
        filtered = queryset.filter(tags__name=value)
        return self._filter(queryset, field, value, filtered)

    def filter_author(self, queryset, field, value):
        filtered = queryset.filter(author__id=value)
        return self._filter(queryset, field, value, filtered)

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'tags',
            'author'
        )
