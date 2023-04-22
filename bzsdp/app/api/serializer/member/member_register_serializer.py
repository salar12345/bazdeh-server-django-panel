from rest_framework import serializers


class MemberRegisterSerializer(serializers.Serializer):
    noence = serializers.CharField(max_length=6, allow_null=False)
    code = serializers.CharField(max_length=4)

    class Meta:
        fields = ['noence', 'code']
