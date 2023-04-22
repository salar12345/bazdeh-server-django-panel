from rest_framework import serializers


class GoldCalculatorSerializer(serializers.Serializer):
    price = serializers.FloatField()
    weight = serializers.FloatField()
    wage = serializers.FloatField()
    wage_type = serializers.CharField()
    tax = serializers.FloatField()
    benefit = serializers.FloatField()

    class Meta:
        fields = ["price",
                  "weight",
                  "wage",
                  "wage_type",
                  "tax"]
