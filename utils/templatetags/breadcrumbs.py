from django import template
from django.template import Node, Variable
from django.utils.encoding import smart_unicode
from django.template.defaulttags import url
from django.template import VariableDoesNotExist
import logging

log = logging.getLogger(__name__)
register = template.Library()


@register.tag
def breadcrumb(parser, token):
    """
    Renders the breadcrumb.
    Examples:
        {% breadcrumb "Title of breadcrumb" url_var %}
        {% breadcrumb context_var  url_var %}
        {% breadcrumb "Just the title" %}
        {% breadcrumb just_context_var %}

    Parameters:
    -First parameter is the title of the crumb,
    -Second (optional) parameter is the url variable to link to, produced by url tag, i.e.:
        {% url person_detail object.id as person_url %}
        then:
        {% breadcrumb person.name person_url %}

    @author Andriy Drozdyuk
    """
    return BreadcrumbNode(token.split_contents()[1:], False)


@register.tag
def breadcrumb_last(parser, token):
    return BreadcrumbNode(token.split_contents()[1:], True)


@register.tag
def breadcrumb_url(parser, token):
    """
    Same as breadcrumb
    but instead of url context variable takes in all the
    arguments URL tag takes.
        {% breadcrumb "Title of breadcrumb" person_detail person.id %}
        {% breadcrumb person.name person_detail person.id %}
    """

    bits = token.split_contents()
    if len(bits) == 2:
        return breadcrumb(parser, token)

    # Extract our extra title parameter
    title = bits.pop(1)
    token.contents = ' '.join(bits)

    url_node = url(parser, token)

    return UrlBreadcrumbNode(title, url_node, False)


@register.tag
def breadcrumb_last_url(parser, token):
    bits = token.split_contents()
    if len(bits) == 2:
        return breadcrumb(parser, token)

    # Extract our extra title parameter
    title = bits.pop(1)
    token.contents = ' '.join(bits)

    url_node = url(parser, token)

    return UrlBreadcrumbNode(title, url_node, True)


class BreadcrumbNode(Node):
    def __init__(self, vars, last):
        """
        First var is title, second var is url context variable
        """
        self.vars = map(Variable, vars)
        self.last = last

    def render(self, context):
        title = self.vars[0].var

        if title.find("'") == -1 and title.find('"') == -1:
            try:
                val = self.vars[0]
                title = val.resolve(context)
            except:
                title = ''

        else:
            title = title.strip("'").strip('"')
            title = smart_unicode(title)

        url = None

        if len(self.vars) > 1:
            val = self.vars[1]
            try:
                url = val.resolve(context)
            except VariableDoesNotExist:
                log.warn("URL does not exist:'%s'", str(val))
                url = None

        return create_crumb(title, url, self.last)


class UrlBreadcrumbNode(Node):
    def __init__(self, title, url_node, last):
        self.title = Variable(title)
        self.url_node = url_node
        self.last = last

    def render(self, context):
        title = self.title.var

        if title.find("'") == -1 and title.find('"') == -1:
            try:
                val = self.title
                title = val.resolve(context)
            except:
                title = ''
        else:
            title = title.strip("'").strip('"')
            title = smart_unicode(title)

        url = self.url_node.render(context)
        return create_crumb(title, url, self.last)


def create_crumb(title, url=None, last=False):
    """
    Helper function
    <li>
        <a href="#">Admin Lab</a> <span class="divider">&nbsp;</span>
    </li>

    """
    divider = "divider"
    if last:
        divider = "divider-last"
    if url:
        crumb = "<li><a href='%s'>%s</a><span class='%s'>&nbsp;</li>" % (url, title, divider)
    else:
        crumb = "<li>%s<span class='%s'>&nbsp;</li>" % (title, divider)
    return crumb
