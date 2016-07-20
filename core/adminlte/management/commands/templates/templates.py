LIST_TEMPLATES = '''
{% extends "adminlte/common_list.html" %}
{% load static %}

{% block table_head %}
    <th class="text-center hidden-sm hidden-xs" style="width:60px;">
        <input type="checkbox" name="checkboxAllRow" class="checkboxAllRow" v-on:click="toggleAllBox"/>
    </th>
<% table_head %>
    <th class="hidden-sm hidden-xs"></th>
{% endblock %}

{% block table_row %}
    <td class="text-center hidden-sm hidden-xs">
        ##[$index+1]
        <input type="checkbox" class="minimal" name="checkboxRow" value="#[item.id]"/>
    </td>
<% table_row %>
    {% block item_buttons %}
    <td class="text-right hidden-sm hidden-xs">
        {% if page_model_perms.view %}
        <a data-toggle="tooltip" data-placement="bottom" data-original-title="View" href="#[item.detail_url]" class="btn btn-info btn-sm">
           <i class="fa fa-bars fa-inverse"></i>
        </a>
        {% endif %}
        {% if page_model_perms.change %}
        <a data-toggle="tooltip" data-placement="bottom" data-original-title="Edit" href="#[item.edit_url]" class="btn btn-warning btn-sm">
            <i class="fa fa-pencil fa-inverse"></i>
        </a>
        {% endif %}
        {% if page_model_perms.delete %}
        <a data-toggle="tooltip" data-placement="bottom" data-original-title="Delete" href="javascript:void(0);"
           class="btn btn-danger btn-sm" data-pk="#[item.id]" v-on:click="removeOne">
            <i class="fa fa-trash-o fa-inverse"></i>
        </a>
        {% endif %}
    </td>
    {% endblock %}
{% endblock %}

{% block common_list_footer_page_script %}
    <script type="text/javascript" src="{% static 'js/<% app_name %>/<% model_name %>_list.js' %}"></script>
{% endblock %}
'''

TABLE_HEAD_TEMPLATES = '''    <th>%s</th>
'''

TABLE_ROW_TEMPLATES = '''    <td>{!! item.%s !!}</td>
'''

LIST_JS = '''
var <% model_name %>ListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag: '<% app_name %>:api-<% model_name %>-list',
            detail_api_tag: '<% app_name %>:api-<% model_name %>-detail',
            delete_api_tag: '<% app_name %>:api-<% model_name %>-delete',
            // page
            create_url_tag: '<% app_name %>:<% model_name %>-add',
            list_url_tag:   '<% app_name %>:<% model_name %>-list',
            update_url_tag: '<% app_name %>:<% model_name %>-update',
            detail_url_tag: '<% app_name %>:<% model_name %>-detail'
        }
    }
);
'''

MENU_TEMPLATE='''{% load activelink %}
<li class="treeview active {% ifstartswith '/<% app_name %>/' %}active{% endifstartswith %}">
    <a href="javascript:void(0)">
        <i class='fa fa-cloud'></i>
        <b><% App_name %></b>
        <i class="fa fa-angle-left pull-right"></i>
    </a>
    <ul class="treeview-menu menu-open" style="display: block;">
<% model_menu %>
    </ul>
</li>
'''



MENU_APP_TEMPLATE='''
        {% if perms.<% app_name %>.view_<% model_name %> %}
        <li>
            <a href="{% url '<% app_name %>:<% model_name %>-list' %}">
                <i class="fa fa-circle-o"></i>
                <% MODEL_NAME %>
            </a>
            {% if perms.<% app_name %>.add_<% model_name %> %}
            <a href="{% url '<% app_name %>:<% model_name %>-add' %}" class="pull-right">
                <i class="fa fa-plus" aria-hidden="true"></i>
            </a>
            {%endif%}
        </li>
        {%endif%}
'''