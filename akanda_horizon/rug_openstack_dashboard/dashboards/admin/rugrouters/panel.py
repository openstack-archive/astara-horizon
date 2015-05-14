from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class Rugrouters(horizon.Panel):
    name = _("Routers")
    slug = "rugrouters"


dashboard.Admin.register(Rugrouters)
