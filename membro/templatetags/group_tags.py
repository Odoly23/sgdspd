# membro/templatetags/group_tags.py
from django import template

register = template.Library()

@register.filter
def is_editor(user):
    allowed = ['ald', 'postu']
    return user.groups.filter(name__in=allowed).exists()