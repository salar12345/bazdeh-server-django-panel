from rest_framework import serializers


class GoldBubbleSerializer(serializers.Serializer):
    right_to_mint_coin = serializers.IntegerField()  #
    dollar_price = serializers.FloatField()  #
    gold_ounce_price = serializers.FloatField()  #
    coin_type = serializers.CharField(max_length=128)  #
    coin_price = serializers.FloatField()  #
    coin_weight = serializers.FloatField(required=False)

    class Meta:
        fields = ['right_to_mint_coin', 'dollar_price', 'gold_ounce_price', 'coin_type', 'coin_price']


