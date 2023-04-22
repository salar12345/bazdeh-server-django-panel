from typing import Dict

from bzscl.model.vo.structure.force_update_vo import ForceUpdateVo
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.structure.force_update_dal import ForceUpdateDal


class ForceUpdateLogic(metaclass=Singleton):
    def __init__(self):
        self.force_update_dal = ForceUpdateDal()

    def get_update_status(self, version: str) -> Dict:
        major, minor, patch = [int(num) for num in version.split('.')]
        filters = {
            ForceUpdateVo.MAJOR: major,
            ForceUpdateVo.MINOR: minor,
            ForceUpdateVo.PATCH: patch
        }
        version = self.force_update_dal.get(**filters)
        return {
            ForceUpdateVo.FORCE_UPDATE: version.force_update,
            ForceUpdateVo.OPTIONAL_UPDATE: self._check_if_version_is_old(major, minor, patch)
        }

    def _check_if_version_is_old(self, major: int, minor: int, patch: int) -> bool:
        bigger_major_filter = {f'{ForceUpdateVo.MAJOR}__gt': major}
        bigger_major_q_object = self.force_update_dal.get_q_object(**bigger_major_filter)
        bigger_minor_filter = {f'{ForceUpdateVo.MAJOR}': major, f'{ForceUpdateVo.MINOR}__gt': minor}
        bigger_minor_q_object = self.force_update_dal.get_q_object(**bigger_minor_filter)
        bigger_patch_filter = {
            f'{ForceUpdateVo.MAJOR}': major,
            f'{ForceUpdateVo.MINOR}': minor,
            f'{ForceUpdateVo.PATCH}__gt': patch
        }
        bigger_patch_q_object = self.force_update_dal.get_q_object(**bigger_patch_filter)
        q_object = bigger_major_q_object | bigger_minor_q_object | bigger_patch_q_object
        return self.force_update_dal.exists(
            qs=self.force_update_dal.filter(q_object)
        )
