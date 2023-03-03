from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..models import MenuItem

register = template.Library()


def get_url(menu_item):
    url = menu_item.url
    if not (url.startswith('http') or url.startswith('https')):
        try:
            url = reverse(url)
        except:
            pass
    return url


def get_is_menu_item_active(menu_item, current_url):
    if get_url(menu_item) == current_url:
        return True
    return False


def get_is_menu_item_active_recursive(menu_item, current_url):
    if get_is_menu_item_active(menu_item, current_url):
        return True

    for child in menu_item.menuitem_set.all():
        if get_is_menu_item_active_recursive(child, current_url):
            return True

    return False


def get_are_children_active(menu_item, current_url):
    for child in menu_item.menuitem_set.all():
        if get_is_menu_item_active_recursive(child, current_url):
            return True

    return False


def render_menu(menu_items, current_url, parent=None):
    menu_html = '<div class="nav-submenu">'
    for item in menu_items.filter(parent=parent):
        url = get_url(item)
        is_menu_active = get_is_menu_item_active(item, current_url)
        are_children_active = get_are_children_active(item, current_url)
        active_class = 'active' if is_menu_active or are_children_active else ''
        is_parent_class = 'is_parent' if parent is None else ''
        menu_html += f"""
                    <div class="nav-menu-item {active_class} {is_parent_class}">
                        <a class="nav-menu-link" href="{url}">{item.name}</a>"""

        if item.menuitem_set.all():
            active_class = 'active' if are_children_active else ''
            menu_html += f'<div class="dropdown {active_class}">'
            menu_html += render_menu(menu_items, current_url, parent=item)
            menu_html += '</div>'

        menu_html += '</div>'
    menu_html += '</div>'
    return menu_html


@register.simple_tag(takes_context=True)
def nav_menu(context, menu_name="main"):
    menu_name = 'main' if not menu_name else menu_name
    menu_items = MenuItem.objects.filter(menu_name=menu_name)
    current_url = context['request'].path

    rendered_menu = render_menu(menu_items, current_url)
    menu_html = f"""<div class="nav-menu">{rendered_menu}</div>"""

    return mark_safe(menu_html)
