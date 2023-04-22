from bzscl.model.entity.system.system_config_entity import SystemConfigEntity
from rest_framework import serializers


class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfigEntity
        fields = '__all__'