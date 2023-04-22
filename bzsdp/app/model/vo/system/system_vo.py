from bzsdp.app.model.vo.base_vo import BaseVO


class SystemVO(BaseVO):
    MEMEBER_ID = 'memeber_id'
    VISUAL_ITEM_LAST_UPDATE_TIME = 'visual_item_last_update_time'
    APP_CONFIG_LAST_UPDATE_TIME = 'app_config_last_update_time'
    GPS_ADID = 'device_gps_adid'
    VERSION = 'version'
    SEND_DEVICE = "send_device"
    FORCE_UPDATE = "force_update"
    OPTIONAL_UPDATE = "optional_update"
    PARTICIPATE_VOTE = "participate_vote"
    VISUAL_ITEMS = "visual_items"
    APP_CONFIGS = "app_configs"
    STRUCTURE_RESULT = "structure_result"
    HOME_PAGE_CONFIG = "home_page_config"
    TOKEN_RESULT = 'token_result'
    HOME_PAGE = 'home_page'
    VERSION_TYPE = 'version_type'
    SPECIAL_PAGES = 'special_pages'
    UNSEEN_GAME_RESULT = 'unseen_game_result'
    VOTE_QUESTION = 'vote_question'
    APP_CONFIG_AND_VISUAL_ITEM_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

