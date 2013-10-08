__author__ = 'jinguangzhou'
from django.conf.urls import patterns, url

from nb_webapp import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       #url(r'^register/$', views.RegisterView.as_view(), name='Sign up'),
                       url(r'^register/$', views.register, name='Register'),
                       url(r'^informationFromFriends', views.flowingInfo, name='flowingInfo'),
                       url(r'^login_signup', views.loginsignup, name = 'loginsignup'),
                       url(r'^login', views.login, name = 'login'),
                       url(r'^signup', views.signup, name = 'signup'),
)
