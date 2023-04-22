from ncl.utils.common.singleton import Singleton
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bzsdp.app.api.controller.base_api_view import BasePanelController
from bzsdp.app.api.serializer.content.special_news.special_subjects_serializer import SpecialSubjectsSerializer

from bzsdp.app.api.serializer.system.startup_serializer import StartupSerializer
from bzsdp.app.api.serializer.system.system_serializer import SystemConfigSerializer
from bzsdp.app.api.serializer.system.visual_item_serializer import VisualItemSerializer
from bzsdp.app.logic.content.special_page_logic import SpecialPageLogic
from bzsdp.app.logic.structure.force_update_logic import ForceUpdateLogic
from bzsdp.app.logic.interaction.vote.vote_logic import VoteLogic
from bzsdp.app.logic.interaction.game_vote_logic import GameVoteLogic

from bzsdp.app.logic.interaction.interaction_logic import InteractionLogic
from bzsdp.app.logic.member.member_logic import MemberLogic
from bzsdp.app.logic.structure.structure_logic import StructureLogic
from bzsdp.app.logic.system.system_logic import SystemLogic
from bzsdp.app.model.vo.member.member_vo import MemberVO
from bzsdp.app.model.vo.system.system_vo import SystemVO


class StartupController(BasePanelController, APIView, metaclass=Singleton):

    def __init__(self):
        super().__init__()

        self.system_logic = SystemLogic()
        self.interaction_logic = InteractionLogic()
        self.structure_logic = StructureLogic()
        self.member_logic = MemberLogic()
        self.special_page_logic = SpecialPageLogic()
        self.force_update_logic = ForceUpdateLogic()
        self.vote_logic = VoteLogic()
        self.game_vote_logic = GameVoteLogic()

    def get(self, request, format=None):
        device = request.query_params
        serializer = StartupSerializer(data=device)
        configs = {}
        done_vote = False

        if serializer.is_valid():
            member = self.get_current_member(request)
            token = request.headers.get(SystemVO.AUTHORIZATION)
            version = serializer.data.get(SystemVO.VERSION)
            gps_adid = serializer.data.get(SystemVO.GPS_ADID)
            if member is None and token:
                return Response({}), 422
            else:
                pass
            token_result = None
            structure_config_result = None
            if not token:
                member = self.member_logic.register_member(phone_number='')
                refresh_token, access_token = self.member_logic.generate_member_token(member=member)
                token_result = {MemberVO.ACCESS_TOKEN: str(access_token), MemberVO.REFRESH_TOKEN: str(refresh_token)}
                active_configs = self.structure_logic.get_active_configs()
                if active_configs:
                    structure_config_result = self.structure_logic.determine_version_percentage(member=member,
                                                                                                active_configs=active_configs)

            if serializer.data.get(SystemVO.VISUAL_ITEM_LAST_UPDATE_TIME) == '':
                visual_item_last_update_time = None
            else:
                visual_item_last_update_time = serializer.data.get(SystemVO.VISUAL_ITEM_LAST_UPDATE_TIME)

            visual_item = self.system_logic.get_visual_item(last_update_time=visual_item_last_update_time)
            serialized_visual_item = VisualItemSerializer(visual_item, many=True)

            if serializer.data.get(SystemVO.APP_CONFIG_LAST_UPDATE_TIME) == '':
                app_config_last_update_time = None
            else:
                app_config_last_update_time = serializer.data.get(SystemVO.APP_CONFIG_LAST_UPDATE_TIME)

            # active_vote = self.interaction_logic.get_active_vote()

            system_configs = self.system_logic.get_all_configs_if_needed(last_update_time=app_config_last_update_time)
            serialized_configs = SystemConfigSerializer(system_configs, many=True)

            if version is not None:
                try:
                    update_status = self.force_update_logic.get_update_status(version)
                except Exception:
                    update_status = {
                        SystemVO.FORCE_UPDATE: False,
                        SystemVO.OPTIONAL_UPDATE: False
                    }
            else:
                update_status = {
                    SystemVO.FORCE_UPDATE: False,
                    SystemVO.OPTIONAL_UPDATE: False
                }

            # if version is not None:
            #     vote_question = self.vote_logic.active_question_exists(member, version)
            # else:
            #     vote_question = False
            #
            # if active_vote:
            #     done_vote = self.interaction_logic.get_member_participate(gps_adid=gps_adid)

            if member:
                try:
                    structure_config_result = self.structure_logic.get_ab_test_member_active_config(member=member)
                except Exception:
                    structure_config_result = None

            unseen_game_result = self.game_vote_logic.check_if_member_has_unseen_vote(member)

            # optional_update = self.system_logic.determine_optional_update(version=version)
            total_special_subjects = self.special_page_logic.get_all_special_page_subjects()
            serialized_special_subjects = SpecialSubjectsSerializer(total_special_subjects, many=True)

            configs[SystemVO.VOTE_QUESTION] = False
            configs[SystemVO.VISUAL_ITEMS] = serialized_visual_item.data
            configs[SystemVO.APP_CONFIGS] = serialized_configs.data
            configs[SystemVO.SEND_DEVICE] = True
            configs[SystemVO.STRUCTURE_RESULT] = structure_config_result
            configs[SystemVO.TOKEN_RESULT] = token_result
            configs[SystemVO.PARTICIPATE_VOTE] = False
            configs[SystemVO.SPECIAL_PAGES] = serialized_special_subjects.data
            configs[SystemVO.FORCE_UPDATE] = update_status[SystemVO.FORCE_UPDATE]
            configs[SystemVO.OPTIONAL_UPDATE] = update_status[SystemVO.OPTIONAL_UPDATE]
            configs[SystemVO.UNSEEN_GAME_RESULT] = unseen_game_result

            return Response(configs, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
