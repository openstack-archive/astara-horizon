from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import forms
from horizon import exceptions

from openstack_dashboard import api

from akanda_horizon.rug_openstack_dashboard.dashboards.admin.rugrouters import \
    tables as router_tables
from akanda_horizon.rug_openstack_dashboard.dashboards.admin.rugrouters import \
    forms as rugrouters_forms
from akanda_horizon.rug_openstack_dashboard.api.rug import RugClient


rc = RugClient()


class IndexView(tables.DataTableView):
    table_class = router_tables.RouterTable
    template_name = 'admin/rugrouters/index.html'

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_data(self):
        try:
            routers, self._more = rc.get_routers(self.request)
            return routers
        except Exception:
            url = reverse('horizon:admin:rugrouters:index')
            exceptions.handle(self.request,
                              _('Unable to retrieve routers\' details.'),
                              redirect=url)


class PollView(forms.ModalFormView):
    form_class = rugrouters_forms.PollForm
    template_name = 'admin/rugrouters/poll.html'
    success_url = reverse_lazy('horizon:admin:rugrouters:index')


class RebuildView(forms.ModalFormView):
    form_class = rugrouters_forms.RebuildForm
    template_name = 'admin/rugrouters/rebuild.html'
    success_url = reverse_lazy('horizon:admin:rugrouters:index')

    def get_context_data(self, **kwargs):
        self.router = api.neutron.router_get(self.request,
                                             self.kwargs['router_id'])
        context = super(RebuildView, self).get_context_data(**kwargs)
        context["router_id"] = self.kwargs['router_id']
        context["router_name"] = self.router['name']
        return context

    def get_initial(self):
        return {
            'router_id': self.kwargs['router_id'],
            'router_name': self.get_context_data()['router_name']
        }
