from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from horizon import exceptions

from akanda_horizon.rug_openstack_dashboard.api.rug import RugClient


rc = RugClient()


class TenantFilterAction(tables.FilterAction):
    def filter(self, table, tenants, filter_string):
        q = filter_string.lower()

        def comp(tenant):
            if q in tenant.name.lower():
                return True
            return False

        return filter(comp, tenants)


class TenantManageAction(tables.BatchAction):
    name = "manage"

    def get_default_classes(self):
        classes = super(tables.BatchAction, self).get_default_classes()
        classes += ("btn-danger", )
        return classes

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Manage Tenant",
            u"Manage Tenants",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Managed Tenant",
            u"Managed Tenants",
            count
        )

    def action(self, request, obj_id):
        try:
            rc.tenant_manage(request, obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class TenantDebugAction(tables.BatchAction):
    name = "debug"

    def get_default_classes(self):
        classes = super(tables.BatchAction, self).get_default_classes()
        classes += ("btn-danger", )
        return classes

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Debug Tenant",
            u"Debug Tenants",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Debugged Tenant",
            u"Debugged Tenants",
            count
        )

    def action(self, request, obj_id):
        try:
            rc.tenant_debug(request, obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class TenantsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Name'),
                         link="horizon:admin:rugtenants:tenant")
    description = tables.Column(lambda obj: getattr(obj, 'description', None),
                                verbose_name=_('Description'))
    id = tables.Column('id', verbose_name=_('Project ID'))
    enabled = tables.Column('enabled', verbose_name=_('Enabled'), status=True)

    class Meta:
        name = "tenants"
        verbose_name = _("Tenants")
        row_actions = (TenantDebugAction, TenantManageAction, )
        table_actions = (TenantFilterAction, )
        pagination_param = "tenant_marker"


class RouterManageAction(tables.BatchAction):
    name = "manage"

    def get_default_classes(self):
        classes = super(tables.BatchAction, self).get_default_classes()
        classes += ("btn-danger", )
        return classes

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Manage Router",
            u"Manage Routers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Managed Router",
            u"Managed Routers",
            count
        )

    def action(self, request, obj_id):
        try:
            rc.router_manage(request, obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class RouterDebugAction(tables.BatchAction):
    name = "debug"

    def get_default_classes(self):
        classes = super(tables.BatchAction, self).get_default_classes()
        classes += ("btn-danger", )
        return classes

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Debug Router",
            u"Debug Routers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Debugged Router",
            u"Debugged Routers",
            count
        )

    def action(self, request, obj_id):
        try:
            rc.router_debug(request, obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class RouterUpdateAction(tables.BatchAction):
    name = "update"

    def get_default_classes(self):
        classes = super(tables.BatchAction, self).get_default_classes()
        classes += ("btn-danger", )
        return classes

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Update Router",
            u"Update Routers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Updated Router",
            u"Updated Routers",
            count
        )

    def action(self, request, obj_id):
        try:
            rc.router_update(request, obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class RouterRebuildAction(tables.LinkAction):
    name = "rebuild"
    verbose_name = _("Rebuild Router")
    classes = ("ajax-modal",)

    def get_link_url(self, datum=None):
        return reverse("horizon:admin:rugtenants:rebuild",
                       kwargs={'tenant_id': datum.tenant_id,
                               'router_id': datum.id})


class TenantRouterTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"),
                         link="horizon:admin:routers:detail")
    status = tables.Column("status", verbose_name=_("Status"))
    latest = tables.Column('latest', verbose_name=_("Latest"))
    image_name = tables.Column('image_name', verbose_name=_("Image Name"))
    last_fetch = tables.Column('last_fetch', verbose_name=_("Last Fetch"))
    booted = tables.Column('booted', verbose_name=_("Booted"))

    class Meta:
        name = "routers"
        verbose_name = _("Routers")
        table_actions = (RouterManageAction, RouterDebugAction, )
        status_columns = ('status',)
        row_actions = (RouterRebuildAction, RouterUpdateAction,
                       RouterManageAction, RouterDebugAction, )
