from typing import Any

from bzscl.model.entity.structure.ab_test_config_entity import AbTestConfigEntity
from bzscl.model.entity.structure.visual_item_entity import VisualItemEntity
from bzscl.model.entity.system.system_config_entity import SystemConfigEntity
from bzscl.model.enum.content.bourse_category_type import BourseCategoryType
from bzscl.model.enum.content.fara_bourse_category_type import FaraBourseCategoryType

from bzscl.model.enum.content.investment_category_type import InvestmentCategoryType
from bzscl.model.enum.content.news_general_category_type import NewsGeneralCategoryGroupType
from bzscl.model.enum.structure.app_component import ComponentGrandParent, ComponentParent, ComponentChild
from bzscl.model.enum.structure.system_config_type import SystemConfigType
from bzscl.model.enum.system.version_type import VersionType

from django.core.management import BaseCommand
from ntl.model.amalgam.priceable_enums import AFRAEcoPriceableType
from ntl.model.amalgam.priceable_pair_type import AFRAPriceablePairType

from bzsdp.project.config import BZSDPConfig
from django.db import transaction


@transaction.atomic
def initial_db():
    ordinal = 0
    for item in NewsGeneralCategoryGroupType:
        ordinal += 1

        VisualItemEntity.objects.get_or_create(code=item.value, display_ordinal=ordinal, fa_name=None, en_name=None,
                                               parent_code=None,
                                               icon_url_path=BZSDPConfig.BASE_URL_PATH + item.name + '.png',
                                               is_active=False)

    for item in InvestmentCategoryType:
        ordinal = ordinal + 1

        parent_code = NewsGeneralCategoryGroupType.BZ_INVESTMENTFUND.value
        VisualItemEntity.objects.get_or_create(code=item.value, display_ordinal=ordinal, fa_name=None, en_name=None,
                                               parent_code=parent_code,
                                               icon_url_path=BZSDPConfig.BASE_URL_PATH + item.name + '.png',
                                               is_active=False)

    for item in AFRAEcoPriceableType:
        if item.fa_name is None:
            item.fa_name = item.db_value
        ordinal = ordinal + 1

        parent_code = NewsGeneralCategoryGroupType.find_priceable_category(item)
        if parent_code:
            parent_code = parent_code.value
        is_target_uri = False
        for pairtype in AFRAPriceablePairType:
            if pairtype.first_side.db_value == item.name:
                is_target_uri = True
                break
        VisualItemEntity.objects.get_or_create(code=item.db_value, display_ordinal=ordinal, fa_name=item.fa_name,
                                               en_name=item.en_name,
                                               parent_code=parent_code,
                                               icon_url_path=BZSDPConfig.BASE_URL_PATH + item.name + '.png',
                                               is_active=True,
                                               is_target_uri=is_target_uri)

    for item in BourseCategoryType:
        ordinal = ordinal + 1

        VisualItemEntity.objects.get_or_create(code=item.value, display_ordinal=ordinal, fa_name=item.fa_name,
                                               en_name=None,
                                               parent_code=item.parent,
                                               icon_url_path="", is_active=True,
                                               is_target_uri=True)

    for item in FaraBourseCategoryType:
        ordinal = ordinal + 1

        VisualItemEntity.objects.get_or_create(code=item.value, display_ordinal=ordinal, fa_name=item.fa_name,
                                               en_name=None,
                                               parent_code=item.parent,
                                               icon_url_path="", is_active=True,
                                               is_target_uri=True)

    for item in SystemConfigType:
        SystemConfigEntity.objects.get_or_create(config_type=item.value, value_str=item.value_str,
                                                 value_int=item.value_int)

    for item in ComponentGrandParent:
        AbTestConfigEntity.objects.get_or_create(component_child=item.value)
        AbTestConfigEntity.objects.get_or_create(component_child=item.value, version_type=VersionType.beta.value,
                                                 percentage=0)

    for item in ComponentParent:
        AbTestConfigEntity.objects.get_or_create(component_child=item.value, componen_parent=item.parent[0].value)
        AbTestConfigEntity.objects.get_or_create(component_child=item.value, componen_parent=item.parent[0].value,
                                                 version_type=VersionType.beta.value, percentage=0)
    for item in ComponentChild:
        AbTestConfigEntity.objects.get_or_create(component_child=item.value, componen_parent=item.parent.value,
                                                 component_grand_parent=item.grand_parent.value)
        AbTestConfigEntity.objects.get_or_create(component_child=item.value, componen_parent=item.parent.value,
                                                 component_grand_parent=item.grand_parent.value,
                                                 version_type=VersionType.beta.value, percentage=0)


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        initial_db()
