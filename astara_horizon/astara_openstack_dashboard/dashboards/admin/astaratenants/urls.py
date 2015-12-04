# Copyright (c) 2015 Akanda, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf.urls import patterns
from django.conf.urls import url

from astara_horizon.astara_openstack_dashboard.dashboards.admin.astaratenants \
    import views

TENANT = r'^(?P<tenant_id>[^/]+)/%s$'

urlpatterns = patterns(
    'astara_openstack_dashboard.dashboards.admin.astaratenants.views',
    url(r'^$', views.TenantIndexView.as_view(), name='index'),
    url(TENANT % '$', views.TenantRouterIndexView.as_view(), name='tenant'),
    url(r'^(?P<tenant_id>[^/]+)/(?P<router_id>[^/]+)/rebuild$',
        views.RebuildView.as_view(), name='rebuild'),
)
