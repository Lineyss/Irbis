from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr: str):
    """Фильтр Jinja для получения значения из поля по его названию

    Args:
        obj (_type_): объект, у которого нужно получить значение
        attr (str): название поля, значение которого необходимо

    Returns:
        _type_: значение поля attr у объекта obj
    """
    return getattr(obj, attr, None)

@register.filter
def get_comp_quantity(comp, compose_attr):
    composed_item = getattr(comp, compose_attr[:len(compose_attr)-3:])
    return getattr(composed_item, 'quantity')