from datetime import date, timedelta, datetime
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_multiple_model.views import ObjectMultipleModelAPIView
from app.models import ChannelModel, ProgrammeModel, TokenModel, ChannelTokenModel
from app.serializers import ChannelSerializer, ProgrammeSerializer, ProgrammeForJsonSerializer, \
    ChannelForFileSerializer, ProgrammeForFileSerializer, TokenSerializer


class ChannelView(APIView):
    serializer_class = ChannelSerializer

    def get(self, request):
        channels = ChannelModel.objects.all()
        return Response(ChannelSerializer(channels, many=True).data)

    def post(self, request):
        serialized = ChannelSerializer(data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response('Parse done channels')


class ProgrammeView(APIView):
    serializer_class = ProgrammeSerializer

    def get(self, request):
        programme = ProgrammeModel.objects.all()
        return Response(ProgrammeSerializer(programme, many=True).data)

    def post(self, request):
        serialized = ProgrammeSerializer(data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response('Parse done programmes')


class EpgDayView(ObjectMultipleModelAPIView):

    def get_querylist(self):
        epg_id = self.request.query_params['id']
        day = self.request.query_params['day'].replace('.', '-')
        querylist = [
            {'queryset': ProgrammeModel.objects.filter(channel_id=epg_id, date_start=day),
             'serializer_class': ProgrammeForJsonSerializer,
             'label': 'data'
             },
        ]
        return querylist


class FileChannelsView(APIView):
    serializer_class = ChannelForFileSerializer

    def get(self, *args, **kwargs):
        token = kwargs.get('token')
        id_user = TokenModel.objects.get(token=token).id
        if id_user is None:
            return Response({"msg": "Token not found"})
        channels = ChannelModel.objects.filter(channeltokenmodel__token_id=id_user)
        return Response(ChannelForFileSerializer(channels, many=True).data)


class FileProgrammesView(APIView):
    serializer_class = ProgrammeForFileSerializer

    def get(self, *args, **kwargs):
        token = kwargs.get('token')
        id_user = TokenModel.objects.get(token=token).id
        if id_user is None:
            return Response({"msg": "Token not found"})
        channel = kwargs.get('pk')
        day = ChannelTokenModel.objects.filter(channel=channel, token=id_user).values_list('day', flat=True).get()
        programmes = ProgrammeModel.objects.filter(channel_id=channel,
                                                   date_start__gt=date.today() - timedelta(days=day),
                                                   date_stop__lt=date.today() + timedelta(days=1)
                                                   )

        return Response(ProgrammeForFileSerializer(programmes, many=True).data)


class AllView(ObjectMultipleModelAPIView):

    def get_querylist(self):
        token = self.kwargs.get('token')
        id_user = TokenModel.objects.get(token=token).id
        now_unix = datetime.now().strftime('%s')
        print(now_unix)
        if id_user is None:
            return Response({"msg": "Token not found"})

        querylist = (
            {'queryset': ChannelModel.objects.filter(channeltokenmodel__token_id=id_user),
             'serializer_class': ChannelForFileSerializer,
             'label': 'channels'
             },
            {'queryset': ProgrammeModel.objects.filter(channel_id__channeltokenmodel__token=id_user,
                                                       begin__gt=now_unix - F('channel_id__channeltokenmodel__date_select'),
                                                       date_stop__lt=date.today() + timedelta(days=2)
                                                       ),
             'serializer_class': ProgrammeForFileSerializer,
             'label': 'programme'
             }
        )
        return querylist


class TokenView(APIView):
    serializer_class = TokenSerializer

    def get(self, request):
        token = TokenModel.objects.all()
        return Response(TokenSerializer(token, many=True).data)


class DelView(APIView):
    serializer_class = ProgrammeSerializer

    def delete(self, request):
        day = request.query_params['day'].replace('.', '-')
        programme = ProgrammeModel.objects.filter(date_start__lt=day)
        count = programme.count()
        programme.delete()
        return Response({'msg': f"{count} programmes deleted"})
