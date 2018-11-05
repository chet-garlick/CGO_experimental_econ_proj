# urls.py
from django.conf.urls import url
from otree.urls import urlpatterns
from django.conf import urls
import my_matrix_ret.pages as pages  

urlpatterns.append(url(r'^verify/$', pages.verify, name='verify'))
