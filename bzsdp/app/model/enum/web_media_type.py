from enum import Enum, unique

from bzsdp.app.model.vo.adapter.post_vo import PostVo


@unique
class MediaType(Enum):
    IMAGE = (0, PostVo.IMAGE)
    VIDEO = (1, PostVo.VIDEO)

    def __init__(self, grpc_code: int, media_type_value: str):
        self.grpc_code = grpc_code
        self.media_type_value = media_type_value

    @classmethod
    def get_grpc_code_from_media_type_value(cls, media_type_value: str) -> int:
        if not isinstance(media_type_value, str):
            raise TypeError
        for media_type in cls.__members__.values():
            if media_type.media_type_value == media_type_value:
                return media_type.grpc_code
        raise ValueError


    @classmethod
    def get_media_type_from_grpc_code(cls, grpc_code: int):
        if not isinstance(grpc_code, int):
            raise TypeError
        for media_type in cls.__members__.values():
            if media_type.grpc_code == grpc_code:
                return media_type.media_type_value
        raise ValueError
