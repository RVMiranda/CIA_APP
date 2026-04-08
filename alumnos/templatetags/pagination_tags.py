from django import template

register = template.Library()

@register.simple_tag
def get_elided_page_range(paginator, number, on_each_side=2, on_ends=1):
    """
    Simula o delega la paginación con elipsis de forma compatible.
    Si la versión de Django (3.2+) lo soporta de forma nativa, lo aprovecha.
    Si no, usa esta implementación idéntica.
    """
    if hasattr(paginator, 'get_elided_page_range'):
        return paginator.get_elided_page_range(number, on_each_side=on_each_side, on_ends=on_ends)

    if paginator.num_pages <= (on_each_side + on_ends) * 2 + 1:
        return paginator.page_range

    page_range = []

    if number <= (on_each_side + on_ends + 1):
        page_range.extend(range(1, on_each_side * 2 + on_ends + 2))
        page_range.append(paginator.ELLIPSIS)
        page_range.extend(range(paginator.num_pages - on_ends + 1, paginator.num_pages + 1))
    elif number > (paginator.num_pages - on_each_side - on_ends - 1):
        page_range.extend(range(1, on_ends + 1))
        page_range.append(paginator.ELLIPSIS)
        page_range.extend(range(paginator.num_pages - on_each_side * 2 - on_ends, paginator.num_pages + 1))
    else:
        page_range.extend(range(1, on_ends + 1))
        page_range.append(paginator.ELLIPSIS)
        page_range.extend(range(number - on_each_side, number + on_each_side + 1))
        page_range.append(paginator.ELLIPSIS)
        page_range.extend(range(paginator.num_pages - on_ends + 1, paginator.num_pages + 1))

    return page_range

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Construye de forma mágica la string a añadir en la Query, preservando todos los filtros (por ejemplo: q=Juan&estado=Activo) e integrando de paso la variable de "page".
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
