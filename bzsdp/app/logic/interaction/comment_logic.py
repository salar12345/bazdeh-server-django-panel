import uuid
from json import dumps, loads
from typing import Dict, Optional, Union

from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.interaction.comment_entity import CommentEntity
from bzscl.model.vo.interaction.comment_vo import CommentVo
from bzscl.model.enum.structure.app_component import ComponentGrandParent, ComponentParent
from ncl.utils.common.singleton import Singleton

from bzsdp.app.data.dal.content.comment_dal import CommentDal
from bzsdp.app.data.dal.member.member_dal import MemberDal
from bzsdp.app.adapter.grpc.ghasedak.ghasedak_adapter import GhasedakAdapter
from bzsdp.app.model.vo.member.device_vo import DeviceVO


class CommentLogic(metaclass=Singleton):
    def __init__(self):
        self.comment_dal = CommentDal()
        self.member_dal = MemberDal()
        self.ghasedak_adapter = GhasedakAdapter()

    def delete_comment(self, member: MemberEntity, comment_id: str) -> None:
        comment_filter = {
            CommentVo.MEMBER: member,
            CommentVo.ID: comment_id
        }
        self.comment_dal.delete(self.comment_dal.get(**comment_filter))

    @staticmethod
    def _validate_parent_comment_indent(parrent_comment: CommentEntity) -> bool:
        return True if parrent_comment.reply_to is None else False

    def get_comment(self, id_: str) -> CommentEntity:
        return self.comment_dal.get_by_id(id_)

    def check_if_user_has_commented_before(self, member: MemberEntity) -> bool:
        return self.comment_dal.exists(member=member)

    def add_comment(
            self,
            member: MemberEntity,
            content: str,
            news_or_analysis_id: str,
            first_comment: bool,
            jwt_token: Optional[str] = None,
            reply_to: Optional[CommentEntity] = None,
            mentioned_member: Optional[MemberEntity] = None
    ) -> Union[CommentEntity, None]:
        if first_comment:
            data = {
                CommentVo.CONTENT: content,
                CommentVo.NEWS_OR_ANALYSIS_ID: news_or_analysis_id,
            }
            if reply_to:
                if not self._validate_parent_comment_indent(reply_to):
                    raise Exception('Invalid comment to reply.')
                data[CommentVo.REPLY_TO] = str(reply_to.id)
            if mentioned_member:
                data[CommentVo.MENTIONED_MEMBER] = str(mentioned_member.id)
            self.comment_dal.cache_comment(jwt_token, dumps(data))
        else:
            if reply_to:
                if not self._validate_parent_comment_indent(reply_to):
                    raise Exception('Invalid comment to reply.')
                self.send_comment_notification(comment_id=reply_to.id)
            comment = self.comment_dal.create(member, content, news_or_analysis_id, reply_to, mentioned_member)
            if mentioned_member:
                self._send_mention_notification(mentioned_member, member, content)
            return comment

    def insert_cached_comment_to_db(self, member: MemberEntity, jwt_token: str) -> CommentEntity:
        cached_data: Dict = loads(self.comment_dal.get_cached_comment(jwt_token))
        cached_data['member'] = member

        if parrent_comment_id := cached_data.get(CommentVo.REPLY_TO):
            cached_data.update({CommentVo.REPLY_TO: self.comment_dal.get_by_id(parrent_comment_id)})
            self.send_comment_notification(comment_id=parrent_comment_id)

        if mentioned_member_id := cached_data.get(CommentVo.MENTIONED_MEMBER):
            mentioned_member = self.member_dal.get_member_by_id(mentioned_member_id)
            cached_data.update({CommentVo.MENTIONED_MEMBER: mentioned_member})

        comment = self.comment_dal.create(**cached_data)

        if mentioned_member_id := cached_data.get(CommentVo.MENTIONED_MEMBER):
            mentioned_member = self.member_dal.get_member_by_id(mentioned_member_id)
            self._send_mention_notification(mentioned_member, member, comment.content)

        return comment

    def do_upvote_or_downvote(self, member: MemberEntity, comment_id: uuid, upvote_or_downvote: bool):
        member_comment_state = self.member_comment_upvote_downvote_state(member=member, comment_id=comment_id)
        if member_comment_state == None:
            self.comment_dal.create_reaction(member=member, comment_id=comment_id,
                                             upvote_or_downvote=upvote_or_downvote)
            if upvote_or_downvote is True:
                self.send_comment_notification(comment_id=comment_id)
        else:
            if member_comment_state == True:
                boolean_state = True
            else:
                boolean_state = False

            if boolean_state == upvote_or_downvote:
                self.comment_dal.delete_reaction(member=member, comment_id=comment_id)
            else:
                self.comment_dal.delete_reaction(member=member, comment_id=comment_id)
                self.comment_dal.create_reaction(member=member, comment_id=comment_id,
                                                 upvote_or_downvote=upvote_or_downvote)
        return self.member_comment_upvote_downvote_state(member=member, comment_id=comment_id)

    def member_comment_upvote_downvote_state(self, member: MemberEntity, comment_id: uuid):
        comment_upvote_model = self.comment_dal.exists_reaction(member=member, comment_id=comment_id,
                                                                upvote_or_downvote=True)
        comment_downvote_model = self.comment_dal.exists_reaction(member=member, comment_id=comment_id,
                                                                  upvote_or_downvote=False)
        if comment_upvote_model:
            return True
        elif comment_downvote_model:
            return False
        else:
            return None

    def get_news_or_analysis_comments(self, member: MemberEntity, news_or_analysis_id: str):
        comments = self.comment_dal.get_news_or_analysis_comments(news_or_analysis_id=news_or_analysis_id)
        for comment in comments:
            commenter = self.member_dal.get_member_by_id(member_id=comment.member_id)
            comment.commenter_name = commenter.name
            comment.commenter_last_name = commenter.last_name
            comment.commenter_image_url = commenter.image_url
            comment.commenter_tag = commenter.tag
            comment.upvote_count = self.count_reaction(comment_id=comment.id, upvote_or_downvote=True)
            comment.state = self.member_comment_upvote_downvote_state(member=member, comment_id=comment.id)
            comment.replies = self.get_comment_replies(comment_id=comment.id)
            for reply in comment.replies:
                replier = self.member_dal.get_member_by_id(member_id=reply.member_id)
                reply.commenter_name = replier.name
                reply.commenter_last_name = replier.last_name
                reply.commenter_image_url = replier.image_url
                reply.commenter_tag = replier.tag
                if reply.mentioned_member:
                    reply.father_name = reply.mentioned_member.name
                    reply.father_last_name = reply.mentioned_member.last_name
                    reply.father_tag = reply.mentioned_member.tag
                else:
                    reply.father_name = None
                    reply.father_last_name = None
                    reply.father_tag = None

                reply.upvote_count = self.count_reaction(comment_id=reply.id, upvote_or_downvote=True)
                reply.state = self.member_comment_upvote_downvote_state(member=member, comment_id=reply.id)
        return comments

    def get_comment_replies(self, comment_id):
        return self.comment_dal.get_comment_replies(comment_id=comment_id)

    def count_reaction(self, comment_id: uuid, upvote_or_downvote: bool):
        return self.comment_dal.count_reaction(comment_id=comment_id, upvote_or_downvote=upvote_or_downvote)

    def get_comment_by_id(self, comment_id: uuid):
        return self.comment_dal.get_comment_by_id(comment_id=comment_id)

    def send_comment_notification(self, comment_id: uuid):
        comment = self.get_comment_by_id(comment_id=comment_id)
        member_id = comment.member_id
        news_or_analysis_id = comment.news_or_analysis_id

    def _send_mention_notification(self, reciever: MemberEntity, sender: MemberEntity, content: str):
        template = '{sender_identity} پاسخ داد: {content}'
        sender_identity = f'{sender.name} {sender.last_name} ({sender.tag})'
        push_token_list = [obj[DeviceVO.PUSH_TOKEN] for obj in reciever.devices.all().values(DeviceVO.PUSH_TOKEN)]
        notification_content = template.format(sender_identity=sender_identity, content=content)
        self.ghasedak_adapter.send_ghasedak_notification(
            push_token_list,
            'بازده',
            notification_content,
            grand_parent=ComponentGrandParent.BZ_PROFILE,
            parent=ComponentParent.NOTIFICATION_LIST
        )
