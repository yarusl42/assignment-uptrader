from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..models import MenuItem

register = template.Library()


def build_menu_tree(menu_items):
    menu_dict = {}
    for item in menu_items:
        menu_dict[item.id] = {
            'item': item,
            'children': []
        }
    for item_id, item_dict in menu_dict.items():
        parent_id = item_dict['item'].parent_id
        if parent_id is not None:
            menu_dict[parent_id]['children'].append(item_id)
    return menu_dict


def build_tree(data):
    nodes = {}
    for id, item in data.items():
        nodes[id] = {'item': item['item'], 'children': [], 'parent_id': None, 'id': id}

    for id, item in data.items():
        for child_id in item['children']:
            nodes[child_id]['parent_id'] = id
            nodes[id]['children'].append(nodes[child_id])

    return [node for node in nodes.values() if node['parent_id'] is None]


def render_item(current_url, item_dict):
    res = ""
    item = item_dict['item']
    url = get_url(item)
    is_menu_active = get_is_menu_item_active(item, current_url)
    are_children_active = get_are_children_active(item_dict, current_url)
    active_class = 'active' if is_menu_active or are_children_active else ''
    is_parent_class = 'is_parent' if not item_dict['parent_id'] else ''
    res += f"""
                    <div class="nav-menu-item {active_class} {is_parent_class}">
                        <a class="nav-menu-link" href="{url}">{item.name}</a>"""
    if item_dict['children']:
        active_class = 'active' if are_children_active else ''
        res += f'<div class="dropdown {active_class}">'
        for child in item_dict['children']:
            res += render_item(current_url, child)
        res += '</div>'
    res += '</div>'
    return res


def render_menu(menu, current_url):
    menu_html = '<div class="nav-submenu">'
    for item_dict in menu:
        menu_html += render_item(current_url, item_dict)
    menu_html += '</div>'
    return menu_html


def get_is_menu_item_active(menu_item, current_url):
    if get_url(menu_item) == current_url:
        return True
    return False


def get_is_menu_item_active_recursive(item, current_url):
    if get_is_menu_item_active(item['item'], current_url):
        return True

    for child in item['children']:
        if get_is_menu_item_active_recursive(child, current_url):
            return True

    return False


def get_are_children_active(item, current_url):
    for child in item['children']:
        if get_is_menu_item_active_recursive(child, current_url):
            return True

    return False


def get_url(menu_item):
    url = menu_item.url
    if not (url.startswith('http') or url.startswith('https')):
        try:
            url = reverse(url)
        except:
            pass
    return url


@register.simple_tag(takes_context=True)
def nav_menu(context, menu_name="main"):
    menu_name = 'main' if not menu_name else menu_name
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    current_url = context['request'].path
    menu_trees = build_tree(build_menu_tree(menu_items))
    menu_html = render_menu(menu_trees, current_url)
    return mark_safe(menu_html)
