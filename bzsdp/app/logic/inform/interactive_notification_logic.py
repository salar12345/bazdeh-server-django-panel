from datetime import datetime
from ordered_set import OrderedSet
from typing import Dict, List

from django.db.models import QuerySet
from ncl.utils.common.singleton import Singleton
from bzscl.model.entity.member.member_entity import MemberEntity
from bzscl.model.entity.interaction.comment_entity import CommentEntity
from bzscl.model.vo.interaction.comment_vo import CommentVo
from bzscl.model.vo.interaction.comment_reaction_vo import CommentReactionVo

from bzsdp.app.data.dal.content.comment_reaction_dal import CommentReactionDal
from bzsdp.app.data.dal.content.comment_dal import CommentDal
from bzsdp.app.data.dal.interaction.game_vote_dal import GameVoteDal
from bzsdp.app.model.vo.inform.interactive_notification_vo import InteractiveNotificationVo
from bzsdp.app.model.vo.interaction.game_vo import GameVo
from bzsdp.app.model.enum.inform.interactive_notification_type import InteractiveNotificationType
from bzsdp.project.config import BZSDPConfig


class InteractiveNotificationLogic(metaclass=Singleton):
    PAGE_SIZE = BZSDPConfig.INTERACTIVE_NOTIFICATION_PAGE_SIZE

    def __init__(self):
        self.comment_reaction_dal = CommentReactionDal()
        self.comment_dal = CommentDal()
        self.game_vote_dal = GameVoteDal()

    def get_member_latest_notifications(self, member: MemberEntity, since: datetime) -> List[Dict]:
        mention_notifications = self._generate_mention_notifications(
            self._get_member_latest_mentions_since(member, since)
        )
        reply_notifications = self._generate_reply_notifications(
            self._get_member_latest_replys_since(member, since)
        )
        upvote_notifications = self._generate_upvote_notifications(
            self._get_member_latest_upvoted_comments(member, since)
        )
        game_result_notifications = self._generate_game_result_notifications(
            self._get_member_latest_vote_results_since(member, since)
        )
        notifications = mention_notifications + reply_notifications + upvote_notifications + game_result_notifications
        return sorted(
            notifications, key=lambda n: n[InteractiveNotificationVo.TIMESTAMP], reverse=True
        )[:self.PAGE_SIZE]

    def _generate_upvote_notifications(self, comments: List[CommentEntity]) -> List[Dict]:
        result = list()
        for comment in comments:
            last_up_vote = self.comment_reaction_dal.last(
                qs=self.comment_reaction_dal.order_by(
                    f'-{CommentReactionVo.CREATION_TIME}',
                    qs=self.comment_reaction_dal.all(qs=comment.commentreactionentity_set.all())
                )
            )
            filters = {CommentReactionVo.COMMENT: comment}
            number_of_up_voters = self.comment_reaction_dal.count(
                qs=self.comment_reaction_dal.filter(**filters)
            )
            notification = {
                InteractiveNotificationVo.TYPE: InteractiveNotificationType.COMMENT_UP_VOTE,
                InteractiveNotificationVo.TIMESTAMP: last_up_vote.creation_time.timestamp(),
                InteractiveNotificationVo.DATETIME: last_up_vote.creation_time,
                InteractiveNotificationVo.DATA: {
                    InteractiveNotificationVo.COMMENT: {
                        InteractiveNotificationVo.COMMENT_ID: comment.id,
                        InteractiveNotificationVo.NEWS_OR_ANALYSIS_ID: comment.news_or_analysis_id,
                    },
                    InteractiveNotificationVo.MEMBER: last_up_vote.member,
                    InteractiveNotificationVo.NUMBER_OF_UP_VOTERS: number_of_up_voters
                }
            }
            result.append(notification)
        return result

    def _get_member_latest_upvoted_comments(self, member: MemberEntity, since: datetime) -> List[CommentEntity]:
        # Dirty code, logic and architecture because of a technical limit or issue on Postgresql
        # Visit https://stackoverflow.com/questions/20582966/django-order-by-filter-with-distinct
        initial_qs = self._get_all_upvotes_to_member_since(member, since)
        ordered_upvotes = self.comment_reaction_dal.order_by(
            f'-{CommentReactionVo.CREATION_TIME}',
            qs=initial_qs
        )
        distinct_upvotes_by_comment = self.comment_reaction_dal.distinct(
            f'{CommentReactionVo.COMMENT}',
            qs=initial_qs
        )
        repeated_in_ordered_upvotes = OrderedSet(ordered_upvotes) - OrderedSet(distinct_upvotes_by_comment)
        latest_distinct_and_ordered_upvotes = sorted(
            OrderedSet(ordered_upvotes) - OrderedSet(repeated_in_ordered_upvotes),
            key=lambda re: re.creation_time.timestamp(),
            reverse=True
        )[:self.PAGE_SIZE]
        return [re.comment for re in latest_distinct_and_ordered_upvotes]

    def _get_all_upvotes_to_member_since(self, member: MemberEntity, since: datetime) -> QuerySet:
        filters = {
            f'{CommentReactionVo.COMMENT}__{CommentVo.MEMBER}': member,
            f'{CommentReactionVo.CREATION_TIME}__lt': since,
            CommentReactionVo.STATUS: True,
        }
        return self.comment_reaction_dal.filter(**filters)

    @staticmethod
    def _generate_mention_notifications(comments: QuerySet) -> List[Dict]:
        result = list()
        for comment in comments:
            notification = {
                InteractiveNotificationVo.TYPE: InteractiveNotificationType.COMMENT_MENTION,
                InteractiveNotificationVo.TIMESTAMP: comment.creation_time.timestamp(),
                InteractiveNotificationVo.DATETIME: comment.creation_time,
                InteractiveNotificationVo.DATA: {
                    InteractiveNotificationVo.COMMENT: {
                        InteractiveNotificationVo.COMMENT_ID: comment.id,
                        InteractiveNotificationVo.NEWS_OR_ANALYSIS_ID: comment.news_or_analysis_id,
                    },
                    InteractiveNotificationVo.MEMBER: comment.member,
                    InteractiveNotificationVo.CONTENT: comment.content
                }
            }
            result.append(notification)
        return result

    def _get_member_latest_mentions_since(self, member: MemberEntity, since: datetime) -> QuerySet:
        return self.comment_dal.order_by(
            f'-{CommentVo.CREATION_TIME}',
            qs=self.comment_dal.filter(mentioned_member=member, creation_time__lt=since)
        )[:self.PAGE_SIZE]

    @staticmethod
    def _generate_reply_notifications(comments: QuerySet) -> List[Dict]:
        result = list()
        for comment in comments:
            notification = {
                InteractiveNotificationVo.TYPE: InteractiveNotificationType.COMMENT_REPLY,
                InteractiveNotificationVo.TIMESTAMP: comment.creation_time.timestamp(),
                InteractiveNotificationVo.DATETIME: comment.creation_time,
                InteractiveNotificationVo.DATA: {
                    InteractiveNotificationVo.COMMENT: {
                        InteractiveNotificationVo.COMMENT_ID: comment.id,
                        InteractiveNotificationVo.NEWS_OR_ANALYSIS_ID: comment.news_or_analysis_id,
                    },
                    InteractiveNotificationVo.MEMBER: comment.member,
                    InteractiveNotificationVo.CONTENT: comment.content
                }
            }
            result.append(notification)
        return result

    def _get_member_latest_replys_since(self, member: MemberEntity, since: datetime) -> QuerySet:
        filters = {CommentVo.MENTIONED_MEMBER: member}
        return self.comment_dal.order_by(
            f'-{CommentVo.CREATION_TIME}',
            qs=self.comment_dal.exclude(
                **filters,
                qs=self.comment_dal.filter(reply_to__member=member, creation_time__lt=since)
            )
        )[:self.PAGE_SIZE]

    @staticmethod
    def _generate_game_result_notifications(votes: QuerySet) -> List[Dict]:
        result = list()
        for vote in votes:
            notification = {
                InteractiveNotificationVo.TYPE: InteractiveNotificationType.RIGHT_GAME_VOTE if
                vote.choice.is_correct else InteractiveNotificationType.WRONG_GAME_VOTE,
                InteractiveNotificationVo.TIMESTAMP: vote.choice.question.prediction_result_date.timestamp(),
                InteractiveNotificationVo.DATETIME: vote.choice.question.prediction_result_date,
                InteractiveNotificationVo.DATA: {
                    InteractiveNotificationVo.GAME_ID: vote.choice.question.id
                }
            }
            result.append(notification)
        return result

    def _get_member_latest_vote_results_since(self, member: MemberEntity, since: datetime) -> QuerySet:
        filters = {
            GameVo.MEMBER: member,
            f'{GameVo.CHOICE}__{GameVo.QUESTION}__{GameVo.PREDICTION_RESULT_DATE}'
            '__lt': since,
            f'{GameVo.CHOICE}__{GameVo.QUESTION}__{GameVo.IS_ACTIVE}': False
        }
        return self.game_vote_dal.order_by(
            f'-{GameVo.CHOICE}__{GameVo.QUESTION}__{GameVo.PREDICTION_RESULT_DATE}',
            qs=self.game_vote_dal.filter(**filters)
        )[:self.PAGE_SIZE]
