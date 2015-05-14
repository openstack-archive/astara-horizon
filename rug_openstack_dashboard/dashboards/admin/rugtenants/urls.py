from django.conf.urls import patterns
from django.conf.urls import url

from rug_openstack_dashboard.dashboards.admin.rugtenants import views

TENANT = r'^(?P<tenant_id>[^/]+)/%s$'

urlpatterns = patterns('rug_openstack_dashboard.dashboards.admin.rugtenants.views',
                       url(r'^$', views.TenantIndexView.as_view(), name='index'),
                       url(TENANT % '$', views.TenantRouterIndexView.as_view(), name='tenant'),
                       url(r'^(?P<tenant_id>[^/]+)/(?P<router_id>[^/]+)/rebuild$', views.RebuildView.as_view(), name='rebuild'),
)