"""
URL configuration for loginapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from login import views
import _mysql_connector # type: ignore

urlpatterns = [
    path('',views.home,name = "home"),
    path('admin/', admin.site.urls),
    path("login/",views.login),
    path("add/",views.add),
    path("achieve/",views.achieve),
    path("mentee/",views.mentee),
    path("mentor/",views.mentor),
    path("success/",views.success),
    path("delete/",views.delete,name = "delete"),
    path("detail/",views.detail),
    path("note/",views.note , name = "addnote"),
    path("back/",views.back),
    path("schedule/",views.schedule , name = "schedule"),
    path("semester/",views.semester),
    path("deletelatest/",views.deletelatest),
    path("forgot/",views.forgot,name = "forgot_password"),
    path("manager/",views.manager),
    path("enter/",views.enter),
    path("viewmarks/",views.viewmarks),
    path("log1",views.log1),
    path("postquestion/",views.postquestion),
    path("createquestion/",views.createquestion),
    path("answer/",views.answer),
    path("viewans/",views.viewans),
    path("ans/",views.ans),
    path("manager_view",views.manager_view),
    path("notes/",views.notes,name = "notes")
]
