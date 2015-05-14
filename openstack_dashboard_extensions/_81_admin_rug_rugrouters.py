# The name of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'rugrouters'
# The name of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'admin'
# The name of the panel group the PANEL is associated with.
PANEL_GROUP = 'rug'

# Python panel class of the PANEL to be added.
ADD_PANEL = \
    'akanda_horizon.rug_openstack_dashboard.dashboards.admin.rugrouters.panel.Rugrouters'
