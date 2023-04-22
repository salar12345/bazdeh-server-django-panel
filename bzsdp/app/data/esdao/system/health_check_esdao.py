from ncl.dal.esdao.base_esdao import BaseESDao
from ncl.utils.common.singleton import Singleton


class HealthCheckESDao(BaseESDao, metaclass=Singleton):
    pass
