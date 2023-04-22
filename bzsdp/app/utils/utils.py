from ncl.utils.helper.common_file_utils import CommonsFileUtils
from ncl.utils.helper.commons_dict_utils import CommonsDictUtils
from ncl.utils.helper.commons_string_utils import CommonsStringUtils
import datetime


class CommonsUtils(CommonsStringUtils, CommonsDictUtils, CommonsFileUtils):

    @classmethod
    def get_datetime_now(cls) -> datetime:
        return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)

    @classmethod
    def get_string_datetime_from_datetime(cls, d, format_: str = None) -> str:
        if format_ is None:
            format_ = "%Y-%m-%dT%H:%M:%S.%f"
        return d.strftime(format_)
