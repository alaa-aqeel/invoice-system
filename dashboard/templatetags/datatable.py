from django import template
from django.urls import reverse_lazy
register = template.Library()


@register.filter
def get_attr(obj: object, attr: str) -> object:
    return getattr(obj, attr)

@register.filter
def create_bread(path: str) -> dict:
    bard = {}
    path_splite = path.strip("/").split("/")
    bard.update({path_splite[0]: reverse_lazy(path_splite[0])})
    for path in path_splite[1:]:
        bard.update({path: "#"})

    return bard.items()