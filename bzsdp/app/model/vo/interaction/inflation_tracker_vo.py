from bzsdp.app.model.vo.base_vo import BaseVO


class InflationTrackerVO(BaseVO):
    ID = '_id'
    PRICEABLE = 'priceable'
    PRICEABLE_NAME = 'priceable_name'
    PRICEABLE_ID = 'priceable_id'
    PRICEABLE_INFO = 'priceable_info'
    PRICE = 'price'
    END_YEAR = 'end_year'
    START_YEAR = 'start_year'
    YEAR = 'year'
    IS_DEFAULT = 'is_default'
    UNIT = 'unit'
    INFLATION_RATE = 'inflation_rate'
    __ALL__ = '__all__'
    INFLATION = 'inflation'
