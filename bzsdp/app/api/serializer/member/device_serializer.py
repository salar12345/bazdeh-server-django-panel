from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    gps_adid = serializers.CharField(max_length=128)
    idfa = serializers.CharField(max_length=128, allow_null=True, required=False)
    os_type = serializers.CharField(max_length=128, allow_null=True)
    device_type = serializers.CharField(max_length=128, allow_null=True)
    app_version = serializers.CharField(max_length=128, allow_null=True)
    os_version = serializers.CharField(max_length=128, allow_null=True)
    push_token = serializers.CharField(max_length=1024, allow_null=True)
    device_manufacturer = serializers.CharField(max_length=1024, allow_null=True)
    device_model_name = serializers.CharField(max_length=1024, allow_null=True)
    package_name = serializers.CharField(max_length=128, allow_null=True)

    class Meta:
        fields = ['gps_adid', 'idfa', 'os_type', 'device_type',
                  'app_version',
                  'os_version',
                  'push_token',
                  'device_manufacturer',
                  'device_model_name',
                  'package_name']
