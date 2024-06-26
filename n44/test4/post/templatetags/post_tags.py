from django import template
from ..models import *


register = template.Library()


@register.simple_tag
def post_categories():
    categories = []
    for category in Post.CATEGORY_CHOICES:
        categories.append(category[0])
    return categories
