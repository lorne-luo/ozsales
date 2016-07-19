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
            add_api_tag: '<% app_name %>:api-<% model_name %>-list',
            list_api_tag: '<% app_name %>:api-<% model_name %>-list',
            delete_api_tag: '<% app_name %>:api-<% model_name %>-delete',
            retrieve_api_tag: '<% app_name %>:api-<% model_name %>-detail',
            update_api_tag: '<% app_name %>:api-<% model_name %>-detail',

            create_url_tag: '<% app_name %>:<% model_name %>-add',
            list_url_tag:   '<% app_name %>:<% model_name %>-list',
            detail_url_tag: '<% app_name %>:<% model_name %>-detail',
            update_url_tag: '<% app_name %>:<% model_name %>-update'
        }
    }
);
'''

MENU_TEMPLATE='''{% load activelink %}
<li class="treeview {% ifstartswith '/<% app_name %>/' %}active{% endifstartswith %}">
    <a href="javascript:void(0)">
        <i class='fa fa-cloud'></i>
        <b><% App_name %></b>
        <i class="fa fa-angle-left pull-right"></i>
    </a>
    <ul class="treeview-menu">
<% model_menu %>
    </ul>
</li>
'''

MENU_APP_TEMPLATE='''        {% if perms.<% app_name %>.add_<% model_name %> or perms.<% app_name %>.change_<% model_name %> %}
        <li>
        <a href="{% url '<% app_name %>:<% model_name %>-list' %}">
                <i class="fa fa-circle-o"></i>
                <% MODEL_NAME %>
            </a>
        </li>
        {%endif%}
'''