from rest_framework import serializers


class StartupSerializer(serializers.Serializer):
    visual_item_last_update_time = serializers.CharField(max_length=80, allow_null=True,required=False)
    app_config_last_update_time = serializers.CharField(max_length=80, allow_null=True, required=False)
    device_gps_adid = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=False)
    version = serializers.CharField(max_length=128, allow_null=True, required=False)

    class Meta:
        fields = '__all__'
