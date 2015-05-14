from datetime import datetime
from django.conf import settings
from horizon.utils import functions as utils
import netaddr
import requests as r
from openstack_dashboard.api.nova import novaclient
from openstack_dashboard.api.neutron import neutronclient


def _mgt_url(host, port, path):
    if ':' in host:
        host = '[%s]' % host
    return 'http://%s:%s%s' % (host, port, path)


def _make_request(url):
    try:
        return r.put(url).ok
    except r.RequestException:
        return False


def _get_local_service_ip(management_prefix):
    mgt_net = netaddr.IPNetwork(management_prefix)
    rug_ip = '%s/%s' % (netaddr.IPAddress(mgt_net.first + 1),
                        mgt_net.prefixlen)
    return rug_ip


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


class RugClient(object):
    def __init__(self):
        self.host = (
            _get_local_service_ip(settings.RUG_MANAGEMENT_PREFIX)
            .split('/')[0]
        )
        self.port = settings.RUG_API_PORT
        self.image_uuid = settings.ROUTER_IMAGE_UUID
        self.api_limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

    def poll(self):
        path = '/poll'
        return _make_request(_mgt_url(self.host, self.port, path))

    def config_reload(self):
        path = '/config/reload'
        return _make_request(_mgt_url(self.host, self.port, path))

    def workers_debug(self):
        path = '/workers/debug'
        return _make_request(_mgt_url(self.host, self.port, path))

    def router_debug(self, router_id):
        path = '/router/debug/{router_id}'.format(router_id=router_id)
        return _make_request(_mgt_url(self.host, self.port, path))

    def router_manage(self, router_id):
        path = '/router/manage/{router_id}'.format(router_id=router_id)
        return _make_request(_mgt_url(self.host, self.port, path))

    def router_update(self, router_id):
        path = '/router/update/{router_id}'.format(router_id=router_id)
        return _make_request(_mgt_url(self.host, self.port, path))

    def router_rebuild(self, router_id, router_image_uuid=None):
        if router_image_uuid:
            path = ('/router/rebuild/{router_id}/--router_image_uuid/' +
                    '{router_image_uuid}').format(
                router_id=router_id,
                router_image_uuid=router_image_uuid
            )
        else:
            path = '/router/rebuild/{router_id}/'.format(router_id=router_id)
        return _make_request(_mgt_url(self.host, self.port, path))

    def tenant_debug(self, tenant_id):
        path = '/tenant/debug/{tenant_id}'.format(tenant_id=tenant_id)
        return _make_request(_mgt_url(self.host, self.port, path))

    def tenant_manage(self, tenant_id):
        path = '/tenant/manage/{tenant_id}'.format(tenant_id=tenant_id)
        return _make_request(_mgt_url(self.host, self.port, path))

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
