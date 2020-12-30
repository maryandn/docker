from rest_framework import serializers

from app.models import ChannelModel, ProgrammeModel, TokenModel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelModel
        fields = ('id', 'name', 'lang')
        extra_kwargs = {'id': {'validators': []}}

    def create(self, validated_data):
        obj = ChannelModel.objects.get_or_create(**validated_data)
        return obj


class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammeModel
        fields = ('channel_id', 'start', 'stop', 'title', 'description')

    def create(self, validated_data):
        ch_id = validated_data.get('channel_id')
        start = validated_data.get('start')
        try:
            obj = ProgrammeModel.objects.get(channel_id=ch_id, start=start)
        except ProgrammeModel.DoesNotExist:
            obj = ProgrammeModel(**validated_data)
            obj.save()
        return obj


class ChannelForJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelModel
        fields = ('epg_id', 'name', 'lang')


class ProgrammeForJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammeModel
        fields = ('begin', 'end', 'title', 'description')


class ChannelForFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelModel
        fields = ('id', 'name', 'lang')


class ProgrammeForFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammeModel
        fields = ('channel_id', 'start', 'stop', 'title')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenModel
        fields = ('token', 'name_service')
