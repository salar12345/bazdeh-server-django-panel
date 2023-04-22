from django.urls import path, include

urlpatterns = [
    path('startup', include('bzsdp.app.api.dispatcher.system.startup_dispatcher')),
    path('health_check', include('bzsdp.app.api.dispatcher.system.health_check_dispatcher')),
    path('auth/', include('bzsdp.app.api.dispatcher.member.member_dispatcher.member_dispatcher')),
    path('', include('bzsdp.app.api.dispatcher.member.device_dispatcher.device_dispatcher')),
    path('watchlist', include('bzsdp.app.api.dispatcher.interaction.watchlist_dispatcher.watchlist_dispatcher')),
    path('loan/', include('bzsdp.app.api.dispatcher.content.loan_dispatcher.loan_dispatcher')),
    path('deposit/', include('bzsdp.app.api.dispatcher.content.deposit_dispatcher.deposit_dispatcher')),
    path('vote/', include('bzsdp.app.api.dispatcher.interaction.vote_dispatcher.vote_dispatcher')),
    path(
        'news_analysis/',
        include('bzsdp.app.api.dispatcher.interaction.news_analysis_like_dispatcher.news_analysis_like_dispatcher')
    ),
    path('portfolio/', include('bzsdp.app.api.dispatcher.member.portfolio_dispatcher.portfolio_dispatcher')),
    path('asset/', include('bzsdp.app.api.dispatcher.member.asset_dispatcher.asset_dispatcher')),
    path('car_price_old/', include('bzsdp.app.api.dispatcher.content.car_price_dispatcher.car_price_dispatcher')),
    path('car/', include('bzsdp.app.api.dispatcher.content.car_price_dispatcher.car_price_dispatcher')),
    path('member_exit', include('bzsdp.app.api.dispatcher.member.member_exit_dispatcher.member_exit_dispatcher')),
    path('user_search', include('bzsdp.app.api.dispatcher.member.user_search_dispatcher.user_search_dispatcher')),
    path('alarm/', include('bzsdp.app.api.dispatcher.inform.price_alarm_dispatcher.price_alarm_dispatcher')),
    path('bookmark/', include('bzsdp.app.api.dispatcher.interaction.bookmark_dispatcher.bookmark_dispatcher')),
    path('', include('bzsdp.app.api.dispatcher.content.home_page_dispatcher.home_page_dispatcher')),
    path('comment/', include('bzsdp.app.api.dispatcher.interaction.comment_dispatcher.comment_dispatcher')),
    path('home_price/', include('bzsdp.app.api.dispatcher.content.home_price_dispatcher.home_price_dispatcher')),
    path('profile', include('bzsdp.app.api.dispatcher.member.profile_dispatcher.profile_dispatcher')),
    path(
        'notification',
        include('bzsdp.app.api.dispatcher.inform.notification_dispatcher.interactive_notification_dispatcher')
    ),
    path(
        'news_analysis_read',
        include('bzsdp.app.api.dispatcher.interaction.news_analysis_read_dispatcher.news_analysis_read_dispatcher')
    ),
    path('', include('bzsdp.app.api.dispatcher.interaction.gold_bubble_dispatcher.gold_bubbler_dispatcher')),
    path('', include('bzsdp.app.api.dispatcher.interaction.gold_calculator_dispatcher.gold_calculator_dispatcher')),
    path('', include('bzsdp.app.api.dispatcher.interaction.member_message_dispatcher.member_message_dispatcher')),
    path('', include('bzsdp.app.api.dispatcher.content.special_page_dispatcher.special_page_dispatcher')),
    path('game/', include('bzsdp.app.api.dispatcher.interaction.game_dispatcher.game_dispatcher')),
    path('search/', include('bzsdp.app.api.dispatcher.interaction.search_dispatcher.search_dispatcher')),
    path(
        'inflation-tracker/',
        include('bzsdp.app.api.dispatcher.interaction.inflation_tracker.inflation_tracker_dispatcher')
    ),
    path('share/', include('bzsdp.app.api.dispatcher.interaction.share.share_dispatcher')),
    path('web_post/', include('bzsdp.app.api.dispatcher.content.web_post_dispatcher.web_post_dispatcher')),
    path('education/', include('bzsdp.app.api.dispatcher.content.education_dispatcher.education_dispatcher')),
    path(
        'risk_measurement/',
        include(
            'bzsdp.app.api.dispatcher.interaction.risk_measurement_dispatcher.risk_measurement_dispatcher'
        )
    ),
    path('analysis/', include('bzsdp.app.api.dispatcher.content.analysis_dispatcher.analysis_dispatcher'))
]
