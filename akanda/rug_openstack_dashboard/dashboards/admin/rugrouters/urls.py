from django.conf.urls import patterns
from django.conf.urls import url

from rug_openstack_dashboard.dashboards.admin.rugrouters import views

ROUTERS = r'^(?P<router_id>[^/]+)/%s$'

urlpatterns = patterns('rug_openstack_dashboard.dashboards.admin.rugrouters.views',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^poll$', views.PollView.as_view(), name='poll'),
                       url(ROUTERS % 'rebuild', views.RebuildView.as_view(), name='rebuild'),
)