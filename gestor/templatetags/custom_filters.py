
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def has_group(user, group_name):
    """
    Verifica si el usuario pertenece al grupo especificado
    Uso: {% if user|has_group:"administrador" %}
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False

@register.simple_tag
def is_admin(user):
    """
    Verifica si el usuario es administrador
    Uso: {% is_admin user as admin_status %}
    """
    if user.is_authenticated:
        return user.groups.filter(name='administrador').exists()
    return False