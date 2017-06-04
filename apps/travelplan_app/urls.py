from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^register$',views.register,name='register'),
    url(r'^login$',views.login,name='login'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^add$',views.add,name='add'),
    url(r'^travels$',views.travels,name='travels'),
    url(r'^showadd$',views.showadd,name='showadd'),
    url(r'^joinTrip/(?P<id>\d+)$',views.joinTrip,name='joinTrip'),
    url(r'^destination/(?P<id>\d+)$',views.destination,name='destination'),
    url(r'^delete$',views.delete,name='delete')

]
