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

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.dashboards.project.images import utils

from astara_horizon.astara_openstack_dashboard.api.astara import AstaraClient


rc = AstaraClient()


def _image_choice_title(img):
    gb = filesizeformat(img.size)
    return '%s (%s)' % (img.name or img.id, gb)


class PollForm(forms.SelfHandlingForm):
    def handle(self, request, data):
        try:
            rc.poll(request)
            messages.success(request, _('Routers were polled'))
        except Exception:
            exceptions.handle(request, _('Unable to poll routers.'))
        return True


class RebuildForm(forms.SelfHandlingForm):
    router_id = forms.CharField(label=_("ID"),
                                widget=forms.HiddenInput(),
                                required=True)
    router_name = forms.CharField(label=_("Router Name"),
                                  widget=forms.HiddenInput(),
                                  required=False)
    attrs = {'class': 'image-selector'}
    image = forms.ChoiceField(label=_("Select Image"),
                              widget=forms.SelectWidget(attrs=attrs,
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
                rc.router_rebuild(request, data['router_id'], data['image'])
            else:
                rc.router_rebuild(request, data['router_id'])
            messages.success(request,
                             _('Rebuilt Router: %s.') % data['router_name'])
        except Exception:
            exceptions.handle(
                request,
                _('Unable to rebuild router %s.' % data['router_name'])
            )
        return True
