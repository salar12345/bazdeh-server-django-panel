from bzsdp.app.model.vo.base_vo import BaseVO


class ShareVo(BaseVO):
    TYPE = 'type_'
    CONTENT = 'content'
    TITLE = 'title'
    SUBTITLE = 'subtitle'
    DESCRIPTION = 'description'
    __ALL__ = '__all__'
    PNG = 'png'
    RAW = 'raw'
    RESULT = 'result'
    IMAGES = 'images'
    LS = 'ls'
    RS = 'rs'
