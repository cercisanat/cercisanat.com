from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()


def process_field(field, field_options):
    if field_options == "placeholder":
        if not 'placeholder' in field.field.widget.attrs:
            field.field.widget.attrs['placeholder'] = unicode(field.label)

    if field_options == "forceplaceholder":
        field.field.widget.attrs['placeholder'] = unicode(field.label)

    else:
        field.field.widget.attrs['placeholder'] = ''


def process_form(element, field_options):
    try:
        for field in element.visible_fields():
            process_field(field, field_options)
    except AttributeError:
        pass


@register.filter
def bootstrap(element, field_options="pass"):
    """
    usage
    {{ form|bootstrap:"field_options" }}

    field_options

    placeholder: sets wigdet attrs['placeholder'] to field.label if no
    placeholder is specified in field definition.

    forceplaceholder: sets wigdet attrs['placeholder'] to field.label even if
    a placeholder attribute is specified in field definition.
        forceplaceholder:custom placeholder

    label: removes placeholders and shows only labels as field label
        label:custom label

    pass: (Default) Does nothing at all. Shows the form as it is defined.

    nolabel: Just displays the field without any label or placeholder.

    """
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        label = None
        if field_options.startswith('label:'):
            label = field_options.replace('label:', '')

        if field_options.startswith('forceplaceholder:'):
            element.label = field_options.replace('forceplaceholder:', '')
            field_options = 'forceplaceholder'

        process_field(element, field_options)
        template = get_template("bootstrapform/field.html")
        context = Context({'field': element,
                           'label': label,
                           'field_options': field_options})
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element:
                process_form(form, field_options)
            template = get_template("bootstrapform/formset.html")
            context = Context({'formset': element,
                               'field_options': field_options})
        else:
            process_form(element, field_options)
            template = get_template("bootstrapform/form.html")
            context = Context({'form': element,
                               'field_options': field_options})

    return template.render(context)


@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"


@register.filter
def is_radio(field):
    return field.field.widget.__class__.__name__.lower() == "radioselect"
