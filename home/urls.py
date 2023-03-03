from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),
    path('child1ofchild1', views.child1ofchild1, name='child1ofchild1'),
    path('child2ofchild1', views.child2ofchild1, name='child2ofchild1'),
    path('child2', views.child2, name='child2'),
    path('child1', views.child1, name='child1'),
    path('page1', views.page1, name='page1'),
    path('page2', views.page2, name='page2'),
]



