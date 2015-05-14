# Akanda Rug Horizon Extension

1. Install module
    
    ```
    pip install akanda-horizon
    ```
    
2. Copy extension files from the project root folder to ```/etc/openstack_dashboard/local/enabled``` or to ```/opt/stack/horizon/openstack_dashboard/local/enabled``` folder

    ```
    cp openstack_dashboard_extensions/*.py /opt/stack/horizon/openstack_dashboard/local/enabled/
    ```

3. Specify rug management prefix, rug api port, and router image uuid in ```local_setting.py```

    ```
    RUG_MANAGEMENT_PREFIX = "fdca:3ba5:a17a:acda::/64"
    RUG_API_PORT = 44250
    ROUTER_IMAGE_UUID = "1e9c16f3-e070-47b7-b49c-ffcf38df5f9a"
    ```
