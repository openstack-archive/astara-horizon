from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class Rugtenants(horizon.Panel):
    name = _("Tenants")
    slug = "rugtenants"


dashboard.Admin.register(Rugtenants)
