
<!-- jinja2 template extends `full` to include cell tags in the html rendering of notebooks -->
{% extends 'full.tpl'%}
{% block any_cell %}
{% if cell['metadata'].get('tags', []) %}
    <div style="background-color:white; border:thin solid grey; margin-left:95px; margin-right:6px">
    {% for tag in cell['metadata'].get('tags', []) %}
        &nbsp; <a href="https://{github_user_name}.github.io/{github_repo_name}/tag_index.html#{{ tag }}">{{ tag }}</a>
    {% endfor %}
    </div>
    {% if 'home-activity' in cell['metadata'].get('tags', []) %}
        <div style="background-color: rgba(0,255,0,0.05) ; padding: 10px; margin-left:95px; margin-right:6px; border: 1px solid darkgreen;"> <b>Home Activity</b>: {{ super() }} </div>
    {% elif 'class-activity' in cell['metadata'].get('tags', []) %}
        <div style="background-color: rgba(0,0,255,0.05) ; padding: 10px; margin-left:95px; margin-right:6px; border: 1px solid darkgreen;"> <b>Class Activity</b>: {{ super() }} </div>
    {% elif 'important-note' in cell['metadata'].get('tags', []) %}
        <div style="background-color: rgba(255,0,0,0.05) ; padding: 10px; margin-left:95px; margin-right:6px; border: 1px solid darkgreen;"> <b>Important Note</b>: {{ super() }} </div>
    {% else %}
        {{ super () }}
    {% endif %}
{% else %}
    {{ super() }}
{% endif %}
{% endblock any_cell %}

