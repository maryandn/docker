from django.contrib import admin
from django.db.models import Count

from .models import ChannelModel, ProgrammeModel, TokenModel, ChannelTokenModel


class TokenAdmin(admin.ModelAdmin):
    list_display = ('name_service', 'token')
    list_filter = ('name_service', 'token')


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('channel_id', 'start', 'stop', 'title')
    list_filter = ('channel_id',)


@admin.register(ChannelModel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pr_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super(ChannelAdmin, self).get_queryset(request)
        return qs.annotate(books_count=Count('programmemodel'))

    def pr_count(self, inst):
        return inst.books_count


@admin.register(ChannelTokenModel)
class ChannelTokenAdmin(admin.ModelAdmin):
    list_display = ['get_name_service', 'day', 'get_channel']
    list_filter = ('token',)

    def get_name_service(self, obj):
        return obj.token.name_service


admin.site.register(ProgrammeModel, ProgrammeAdmin)
admin.site.register(TokenModel, TokenAdmin)

