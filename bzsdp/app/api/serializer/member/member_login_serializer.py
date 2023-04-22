from rest_framework import serializers


class MemberLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=80, allow_null=False)

    class Meta:
        fields = ['phone_number']
