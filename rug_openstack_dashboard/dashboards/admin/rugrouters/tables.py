from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import tables

from rug_openstack_dashboard.api.rug import RugClient


rc = RugClient()


class ManageAction(tables.BatchAction):
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
            rc.router_manage(obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class DebugAction(tables.BatchAction):
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
            rc.router_debug(obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class UpdateAction(tables.BatchAction):

    # todo: single action

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
            rc.router_update(obj_id)
        except Exception:
            msg = _('Failed to manage route %s') % obj_id
            exceptions.handle(request, msg)


class PollAction(tables.LinkAction):
    name = "poll"
    verbose_name = _("Poll Routers")
    url = "horizon:admin:rugrouters:poll"
    classes = ("ajax-modal",)


class RebuildAction(tables.LinkAction):
    name = "rebuild"
    verbose_name = _("Rebuild Router")
    url = "horizon:admin:rugrouters:rebuild"
    classes = ("ajax-modal",)


class RouterTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"), link=("horizon:admin:routers:detail"))
    status = tables.Column("status", verbose_name=_("Status"))
    latest = tables.Column('latest', verbose_name=_("Latest"))
    image_name = tables.Column('image_name', verbose_name=_("Image Name"))
    last_fetch = tables.Column('last_fetch', verbose_name=_("Last Fetch"))
    booted = tables.Column('booted', verbose_name=_("Booted"))

    class Meta:
        name = "routers"
        verbose_name = _("Routers")
        table_actions = (ManageAction, DebugAction, PollAction)
        status_columns = ('status',)
        row_actions = (RebuildAction, UpdateAction, ManageAction, DebugAction, )