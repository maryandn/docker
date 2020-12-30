from django.urls import path

from app.views import ChannelView, ProgrammeView, FileChannelsView, EpgDayView, AllView, FileProgrammesView, \
    DelView, TokenView

urlpatterns = [
    path('get_channels/', ChannelView.as_view()),
    path('get_programmes/', ProgrammeView.as_view()),
    path('epg_day', EpgDayView.as_view()),
    path('get_token_list', TokenView.as_view()),
    path('del_day', DelView.as_view()),
    path('get_for_file/ch/<str:token>', FileChannelsView.as_view()),
    path('get_for_file/pr/<str:token>/<int:pk>', FileProgrammesView.as_view()),
    path('get_for_file/<str:token>', AllView.as_view()),
]
