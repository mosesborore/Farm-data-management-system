from django.template import Library
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from ..models import UNIT_MEASUREMENT, UNIT_RATE_MEASUREMENT, InputCategory

register = Library()


@register.simple_tag(name="unit_measurement_tag")
def unit_measurement_options(selected):
    """
    Create <option></option> tags prepopulated with
    value and name from unit_measurements choices and also add 'selected' in an <option> that's selected
    for instance:
        unit_measurement = (
            ('KG', 'kilogram'),
            )
        <option value="KG">kilograms</option>
    """
    measurement = list(UNIT_MEASUREMENT)
    opt = []
    for i in measurement:
        if selected == i[0]:
            # mark this option selected
            opt.append(
                format_html("""<option value="{}" selected>{}</option>""", i[0], i[1])
            )
        opt.append(format_html("""<option value="{}" >{}</option>""", i[0], i[1]))
    possible_options = conditional_escape("\n").join(opt)
    return mark_safe(possible_options)


@register.simple_tag(name="unit_rate_measurement_tag")
def unit_rate_measurement_options(selected):
    """
    Create <option></option> tags prepopulated with
    value and name from unit_rate_measurements choices and
    also add 'selected' is an <option> tag that's selected
    for instance:
        unit_rate_measurement = (
            ('kg/acre', 'kilogram/acre'),
            ('g/acre', 'g/acre'),
            )
        <option value="kg/acre">kilogram/acre</option>
        if unit_rate_measurement[1][0] == selected:
            <option value="g/acre" selected>g/acre</option>
    """
    rate_measurement = list(UNIT_RATE_MEASUREMENT)
    opt = []
    for i in rate_measurement:
        if selected == i[0]:
            # mark this option selected
            opt.append(
                format_html("""<option value="{}" selected>{}</option>""", i[0], i[1])
            )
        opt.append(format_html("""<option value="{}" >{}</option>""", i[0], i[1]))
    possible_options = conditional_escape("\n").join(opt)
    return mark_safe(possible_options)


@register.simple_tag(name="category_option_tag")
def category_tag(selected_id):
    """
    Create <select>'s <option>(s) with the value [category id] and name [category name]
    and adds 'selected' value in <option> if selected_id == category.id
    """
    try:
        objects = InputCategory.objects.all()
        opt = []

        for obj in objects:
            if obj.id == selected_id:
                # mark this option selected
                opt.append(
                    format_html(
                        """<option value="{}" selected>{}</option>""", obj.id, obj.name
                    )
                )
            opt.append(
                format_html("""<option value="{}">{}</option>""", obj.id, obj.name)
            )
        possible_options = conditional_escape("\n").join(opt)
        return mark_safe(possible_options)
    except InputCategory.DoesNotExist:
        pass
