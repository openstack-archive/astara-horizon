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

from datetime import datetime
from django.conf import settings
from horizon.utils import functions as utils
import requests as r
from openstack_dashboard.api import base
from openstack_dashboard.api.nova import novaclient
from openstack_dashboard.api.neutron import neutronclient


KEYSTONE_SERVICE_NAME = 'astara'


class Router(object):
    id = ''
    name = ''
    status = ''
    latest = ''
    image_name = ''
    last_fetch = ''
    booted = ''

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


class AstaraClient(object):
    def __init__(self):
        self.image_uuid = settings.ROUTER_IMAGE_UUID
        self.api_limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

    def _make_request(self, request, path):
        url = base.url_for(request, KEYSTONE_SERVICE_NAME) + path
        try:
            return r.put(url).ok
        except r.RequestException:
            return False

    def poll(self, request):
        path = '/poll'
        return self._make_request(request, path)

    def config_reload(self, request):
        path = '/config/reload'
        return self._make_request(request, path)

    def workers_debug(self, request):
        path = '/workers/debug'
        return self._make_request(request, path)

    def router_debug(self, request, router_id):
        path = '/router/debug/{router_id}'.format(router_id=router_id)
        return self._make_request(request, path)

    def router_manage(self, request, router_id):
        path = '/router/manage/{router_id}'.format(router_id=router_id)
        return self._make_request(request, path)

    def router_update(self, request, router_id):
        path = '/router/update/{router_id}'.format(router_id=router_id)
        return self._make_request(request, path)

    def router_rebuild(self, request, router_id, router_image_uuid=None):
        if router_image_uuid:
            path = ('/router/rebuild/{router_id}/--router_image_uuid/' +
                    '{router_image_uuid}').format(
                router_id=router_id,
                router_image_uuid=router_image_uuid
            )
        else:
            path = '/router/rebuild/{router_id}/'.format(router_id=router_id)
        return self._make_request(request, path)

    def tenant_debug(self, request, tenant_id):
        path = '/tenant/debug/{tenant_id}'.format(tenant_id=tenant_id)
        return self._make_request(request, path)

    def tenant_manage(self, request, tenant_id):
        path = '/tenant/manage/{tenant_id}'.format(tenant_id=tenant_id)
        return self._make_request(request, path)

    def get_routers(self, request, **search_opts):
        page_size = utils.get_page_size(request)
        paginate = False
        if 'paginate' in search_opts:
            paginate = search_opts.pop('paginate')
            search_opts['limit'] = page_size + 1
        if 'tenant_id' not in search_opts:
            search_opts['all_tenants'] = True

        routers_metadata = []
        nova_client = novaclient(request)
        routers = (
            neutronclient(request)
            .list_routers(**search_opts)
            .get("routers", [])
        )
        for router in routers:
            search_opts = {'name': 'ak-' + router['id'], 'all_tenants': True}
            instances = nova_client.servers.list(True, search_opts=search_opts)
            instance = instances[0] if instances else None
            image = (
                nova_client.images.get(instance.image['id'])
                if instance else None
            )
            routers_metadata.append(Router(
                id=router['id'],
                name=router['name'],
                latest=image.id == self.image_uuid if image else '',
                image_name=image.name if image else '',
                last_fetch=datetime.utcnow(),
                booted=instance.created if instance else '',
                status=router['status'],
                tenant_id=router['tenant_id'],
            ))

        has_more_data = False
        if paginate and len(routers_metadata) > page_size:
            routers_metadata.pop(-1)
            has_more_data = True
        elif paginate and len(routers_metadata) == self.api_limit:
            has_more_data = True

        return routers_metadata, has_more_data
