from rest_framework.renderers import JSONRenderer


class UTF8JSONRenderer(JSONRenderer):
    charset = 'utf-8'