{% extends 'side.html' %}
{% load static %}

{% // block content %}

<div class="page-header">
    <div class="page-title">
        <h4>Product List</h4>
        <h6>Manage your products</h6>
    </div>
</div>

<div class="card">
    <div class="card-body">

        <table class="table datanew">
            <thead>
                <tr>
                    <th>Product Name</th>
                    <th>SKU</th>
                    <th>Category</th>
                    <th>Brand</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Product A</td>
                    <td>SKU123</td>
                    <td>Electronics</td>
                    <td>Samsung</td>
                </tr>
            </tbody>
        </table>

    </div>
</div>

{% endblock %}
