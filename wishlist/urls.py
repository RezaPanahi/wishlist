"""wishlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from myapp import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('wish_item/create', views.createItemPage),
    path('afterItemCreation', views.afterItemCreation),
    path('wish_item/<int:item_id>', views.wish_items),
    path('removeItem/<int:item_id>', views.removeItem),
    path('addOtherUserItem/<int:item_id>', views.addOtherUserItem),
    path('deleteItem/<int:item_id>', views.delete),
    path('logout', views.logout),
]
