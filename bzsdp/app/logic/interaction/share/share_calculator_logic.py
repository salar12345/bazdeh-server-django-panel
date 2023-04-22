from ncl.utils.common.singleton import Singleton
from PIL import Image, ImageFont, ImageDraw
from typing import Dict
from bzsdp.project.config import BZSDPConfig
from bzsdp.app.model.vo.interaction.share_vo import ShareVo
import urllib.request
import os
import string
import random
import arabic_reshaper
from bidi.algorithm import get_display


class ShareCalculatorsLogic(metaclass=Singleton):
    BASE_PATH_FOR_SHARED_IMAGES = BZSDPConfig.BASE_PATH_FOR_SHARED_IMAGES
    PATH_TO_READ_SHARE_IMAGES = BASE_PATH_FOR_SHARED_IMAGES + ShareVo.RAW + '/'
    PATH_TO_WRITE_SHARE_IMAGES = BASE_PATH_FOR_SHARED_IMAGES + ShareVo.RESULT + '/'
    BASE_CONTAINER_PATH_FOR_SHARE = BZSDPConfig.BASE_CONTAINER_PATH_FOR_SHARE
    TITLE_FONT = BZSDPConfig.SHARE_TITLE_FONT
    CONTENT_FONT = BZSDPConfig.SHARE_CONTENT_FONT

    def __init__(self):
        super().__init__()

    def get_share_image_url(self, data: Dict) -> str:
        self._load_remote_files(data)
        return self._make_image_from_data(data)

    def _load_remote_files(self, data: Dict) -> None:
        file_name = f'{data[ShareVo.TYPE].lower()}'

        if not os.path.isdir(f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{ShareVo.IMAGES}/'):
            os.makedirs(f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{ShareVo.IMAGES}/')

        urllib.request.urlretrieve(f'{self.PATH_TO_READ_SHARE_IMAGES}{file_name}_{ShareVo.RAW}.{ShareVo.PNG}',
                                   f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{file_name}_{ShareVo.RAW}.{ShareVo.PNG}')
        urllib.request.urlretrieve(f'{self.BASE_PATH_FOR_SHARED_IMAGES}{self.TITLE_FONT}',
                                   f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{self.TITLE_FONT}')
        urllib.request.urlretrieve(f'{self.BASE_PATH_FOR_SHARED_IMAGES}{self.CONTENT_FONT}',
                                   f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{self.CONTENT_FONT}')

    def _make_image_from_data(self, data: Dict) -> str:
        file_name = f'{data[ShareVo.TYPE].lower()}'
        title_font = ImageFont.truetype(f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{self.TITLE_FONT}', 14)
        content_font = ImageFont.truetype(f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{self.CONTENT_FONT}', 14)

        image = Image.open(f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{file_name}_{ShareVo.RAW}.{ShareVo.PNG}')
        image_editable = ImageDraw.Draw(image)
        title = self._fix_persian_text(data[ShareVo.TITLE])
        image_editable.text((337, 69), title, (55, 55, 55), font=title_font, anchor=ShareVo.RS)

        y_coordinates = 98
        for item in data[ShareVo.CONTENT]:
            x_coordinates = 337
            subtitle = self._fix_persian_text(item[ShareVo.SUBTITLE])
            image_editable.text((x_coordinates, y_coordinates), subtitle, (55, 55, 55),
                                font=content_font, anchor=ShareVo.RS)
            x_coordinates -= 322
            description = self._fix_persian_text(item[ShareVo.DESCRIPTION])
            image_editable.text((x_coordinates, y_coordinates), description, (55, 55, 55),
                                font=content_font, anchor=ShareVo.LS)
            y_coordinates += 23

        final_file_name = f'{ShareVo.RESULT}_{self.get_random_string(6)}.{ShareVo.PNG}'
        save_result_image_to = f'{self.BASE_CONTAINER_PATH_FOR_SHARE}{ShareVo.IMAGES}/{final_file_name}'
        image.save(save_result_image_to, format=ShareVo.PNG)

        image_url = f'{self.PATH_TO_WRITE_SHARE_IMAGES}{final_file_name}'
        return image_url

    @staticmethod
    def get_random_string(length: int) -> str:
        letters = string.ascii_uppercase + "1234567890"
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def _fix_persian_text(self, text: str) -> str:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
