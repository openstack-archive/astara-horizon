from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from horizon import tables
from horizon import exceptions
from horizon import messages
from horizon import forms

from openstack_dashboard import api
from openstack_dashboard import policy

from rug_openstack_dashboard.dashboards.admin.rugtenants import tables as tenant_tables
from rug_openstack_dashboard.dashboards.admin.rugrouters import forms as rugrouters_forms

from rug_openstack_dashboard.api.rug import RugClient


rc = RugClient()


class TenantIndexView(tables.DataTableView):
    table_class = tenant_tables.TenantsTable
    template_name = 'admin/rugtenants/index.html'

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        tenants = []
        marker = self.request.GET.get(
            tenant_tables.TenantsTable._meta.pagination_param, None)
        domain_context = self.request.session.get('domain_context', None)
        if policy.check((("admin", "admin:list_projects"),), self.request):
            try:
                tenants, self._more = api.keystone.tenant_list(
                    self.request,
                    domain=domain_context,
                    paginate=True,
                    marker=marker)
            except Exception:
                self._more = False
                exceptions.handle(self.request,
                                  _("Unable to retrieve project list."))
        elif policy.check((("admin", "identity:list_user_projects"),),
                          self.request):
            try:
                tenants, self._more = api.keystone.tenant_list(
                    self.request,
                    user=self.request.user.id,
                    paginate=True,
                    marker=marker,
                    admin=False)
            except Exception:
                self._more = False
                exceptions.handle(self.request,
                                  _("Unable to retrieve project information."))
        else:
            self._more = False
            msg = \
                _("Insufficient privilege level to view project information.")
            messages.info(self.request, msg)
        return tenants


class TenantRouterIndexView(tables.DataTableView):
    table_class = tenant_tables.TenantRouterTable
    template_name = 'admin/rugtenants/router-index.html'

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_context_data(self, **kwargs):
        context = super(TenantRouterIndexView, self).get_context_data(**kwargs)
        context["tenant_id"] = self.kwargs['tenant_id']
        tenant = api.keystone.tenant_get(self.request, self.kwargs['tenant_id'], admin=True)
        context["title"] = "Routers of tenant \"%s\"" % tenant.name
        return context

    def get_data(self):
        try:
            routers, self._more = rc.get_routers(self.request, tenant_id=self.kwargs['tenant_id'])
            return routers
        except Exception:
            url = reverse('horizon:admin:rugtenants:index')
            exceptions.handle(self.request, _('Unable to retrieve routers\' details.'), redirect=url)


class RebuildView(forms.ModalFormView):
    form_class = rugrouters_forms.RebuildForm
    template_name = 'admin/rugtenants/rebuild.html'
    success_url = reverse_lazy('horizon:admin:rugtenants:index')

    def get_success_url(self):
        return reverse("horizon:admin:rugtenants:tenant", args=(self.kwargs['tenant_id'],))

    def get_context_data(self, **kwargs):
        self.router = api.neutron.router_get(self.request, self.kwargs['router_id'])
        context = super(RebuildView, self).get_context_data(**kwargs)
        context["router_id"] = self.kwargs['router_id']
        context["tenant_id"] = self.kwargs['tenant_id']
        context["router_name"] = self.router['name']
        return context

    def get_initial(self):
        return {
            'router_id': self.kwargs['router_id'],
            'tenant_id': self.kwargs['tenant_id'],
            'router_name': self.get_context_data()['router_name']
        }