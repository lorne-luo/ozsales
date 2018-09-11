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
  <tbody v-for="item in items">
  <tr>
    <td class="text-center hidden-sm hidden-xs">
      ##[$index+1]
      <input type="checkbox" class="minimal" name="checkboxRow" value="#[item.pk]"/>
    </td>
<% table_row %>
    {% block item_buttons %}
      {{ block.super }}
    {% endblock %}
  </tr>
  </tbody>
{% endblock %}

{% block common_list_footer_page_script %}
  <script type="text/javascript" src="{% static 'js/<% app_name %>/<% model_name %>_list.js' %}"></script>
{% endblock %}
'''

TABLE_HEAD_TEMPLATES = '''  <th>%s</th>
'''

TABLE_ROW_TEMPLATES = '''    <td>{!! item.%s !!}</td>
'''

LIST_JS = '''
var <% model_name %>ListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag:   'api:<% model_name %>-list',
            detail_api_tag: 'api:<% model_name %>-detail',
            delete_api_tag: 'api:<% model_name %>-delete',
            // page
            create_url_tag: '<% app_name %>:<% model_name %>-add',
            list_url_tag:   '<% app_name %>:<% model_name %>-list',
            update_url_tag: '<% app_name %>:<% model_name %>-update',
            detail_url_tag: '<% app_name %>:<% model_name %>-detail',
            list_url:       Urls['api:<% model_name %>-list']() + '?'
        }
    }
);
'''

MENU_TEMPLATE='''
<li class="treeview active">
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
      {% if perms.<% app_name %>.add_<% model_name %> %}
      <a href="{% url '<% app_name %>:<% model_name %>-add' %}" class="pull-right"><i class="fa fa-plus" aria-hidden="true"></i></a>
      {%endif%}
      <a href="{% url '<% app_name %>:<% model_name %>-list' %}" class="main"><i class="fa fa-circle-o"></i><% MODEL_NAME %></a>
    </li>
    
    {%endif%}
'''
