from bzsdp.app.model.vo.base_vo import BaseVO


class SearchVo(BaseVO):
    QUERY_STRING = 'query_string'
    PAGE_NUMBER = 'page_number'
    END_DATETIME = 'end_datetime'
    __ALL__ = '__all__'
    CREATION_TIME = 'creation_time'  # todo : this should be somewhere else not here
