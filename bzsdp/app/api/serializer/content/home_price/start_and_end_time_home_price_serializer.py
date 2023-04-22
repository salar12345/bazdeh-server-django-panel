from rest_framework import serializers


class StartAndEndTimeHomePriceSerializer(serializers.Serializer):
    start_month = serializers.IntegerField()  #
    start_year = serializers.IntegerField()  #
    start_fa_month = serializers.CharField()  #
    start_en_month = serializers.CharField()  #
    start_date = serializers.CharField()  #
    end_month = serializers.IntegerField()  #
    end_year = serializers.IntegerField()  #
    end_fa_month = serializers.CharField()  #
    end_en_month = serializers.CharField()  #
    end_date = serializers.CharField()  #

    class Meta:
        fields = ['start_month', 'start_year', 'start_fa_month', 'start_en_month', 'start_date', 'end_month',
                  'end_year', 'end_fa_month', 'end_en_month', 'end_date']
