LIST_TEMPLATES = '''
{% extends "adminlte/common_list.html" %}
{% load static %}

{% block common_list_footer_page_script %}
    <script type="text/javascript" src="{% static 'js/<% app_name %>/<% model_name %>_list.js' %}"></script>
{% endblock %}
'''

LIST_JS = '''
var <% model_name %>ListPageVue = new CommonListPageVue({
        data: {
            list_api_tag: 'api-<% model_name %>-list',
            create_url_tag: '<% model_name %>-add',
            detail_url_tag: '<% model_name %>-detail',
            update_url_tag: '<% model_name %>-update',
            delete_api_tag: '<% model_name %>-delete'
        }
    }
);
'''