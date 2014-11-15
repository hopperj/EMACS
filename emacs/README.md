sayit_like_you
==============

A simple Django app that demonstrates some improvements we suggested for stackoverflow for a class project

{% extends "base.html" %}
{% block content %}
<table class="tempature1">
<thead>
	<tr>
		<th>Time</th>
		<th>Value</th>
	</tr>
	</thead>
	<tbody>

	{% for record in device_1 %}
	<tr>
		<td>{{ record.0 }}</td>
		<td>{{ record.1 }}</td>
	</tr>
	
	{% endfor %}
	</tbody>
</table>

<table class="tempature2">
<thead>
	<tr>
		<th>Time</th>
		<th>Value</th>
	</tr>
	</thead>
	<tbody>

	{% for record in device_2 %}
	<tr>
		<td>{{ record.0 }}</td>
		<td>{{ record.1 }}</td>
	</tr>
	
	{% endfor %}
	</tbody>
</table>
{% endblock %}
