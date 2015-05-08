from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.dashboards.project.images import utils

from rug_openstack_dashboard.api.rug import RugClient


rc = RugClient()


def _image_choice_title(img):
    gb = filesizeformat(img.size)
    return '%s (%s)' % (img.name or img.id, gb)


class PollForm(forms.SelfHandlingForm):
    def handle(self, request, data):
        try:
            rc.poll()
            messages.success(request, _('Routers were polled'))
        except Exception:
            exceptions.handle(request, _('Unable to poll routers.'))
        return True


class RebuildForm(forms.SelfHandlingForm):
    router_id = forms.CharField(label=_("ID"),
                                widget=forms.HiddenInput(),
                                required=True)
    image = forms.ChoiceField(label=_("Select Image"),
            widget=forms.SelectWidget(attrs={'class': 'image-selector'},
                                      data_attrs=('size', 'display-name'),
                                      transform=_image_choice_title),
                                      required=False)

    def __init__(self, request, *args, **kwargs):
        super(RebuildForm, self).__init__(request, *args, **kwargs)
        images = utils.get_available_images(request, request.user.tenant_id)
        choices = [(image.id, image) for image in images]
        if choices:
            choices.insert(0, ("", _("Select Image")))
        else:
            choices.insert(0, ("", _("No images available")))
        self.fields['image'].choices = choices

    def handle(self, request, data):
        try:
            if data['image']:
                rc.router_rebuild(data['router_id'], data['image'])
            else:
                rc.router_rebuild(data['router_id'])
            messages.success(request, _('Rebuilt router %s.') % data['router_id'])
        except Exception:
            exceptions.handle(request, _('Unable to rebuild router %s.' % data['router_id']))
        return True