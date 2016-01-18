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

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import forms
from horizon import exceptions

from openstack_dashboard import api

from astara_horizon.astara_openstack_dashboard.dashboards.admin.astararouters \
    import tables as router_tables
from astara_horizon.astara_openstack_dashboard.dashboards.admin.astararouters \
    import forms as astararouters_forms
from astara_horizon.astara_openstack_dashboard.api.astara import AstaraClient


rc = AstaraClient()


class IndexView(tables.DataTableView):
    table_class = router_tables.RouterTable
    template_name = 'admin/astararouters/index.html'

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_data(self):
        try:
            routers, self._more = rc.get_routers(self.request)
            return routers
        except Exception:
            url = reverse('horizon:admin:astararouters:index')
            exceptions.handle(self.request,
                              _('Unable to retrieve routers\' details.'),
                              redirect=url)


class PollView(forms.ModalFormView):
    form_class = astararouters_forms.PollForm
    template_name = 'admin/astararouters/poll.html'
    success_url = reverse_lazy('horizon:admin:astararouters:index')


class RebuildView(forms.ModalFormView):
    form_class = astararouters_forms.RebuildForm
    template_name = 'admin/astararouters/rebuild.html'
    success_url = reverse_lazy('horizon:admin:astararouters:index')

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
