from django.db import models
import datetime
from datetime import date, timedelta
from django.utils import timezone


class ChannelModel(models.Model):
    class Meta:
        db_table = 'channels'
        ordering = ['id']
        verbose_name_plural = 'Каналы'

    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=60)
    lang = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.id}  {self.name}"


class ProgrammeModel(models.Model):
    class Meta:
        db_table = 'programmes'
        ordering = ['channel_id']
        verbose_name_plural = 'Программы'

    channel_id = models.ForeignKey(ChannelModel, on_delete=models.CASCADE)
    start = models.CharField(max_length=21, db_index=True)
    stop = models.CharField(max_length=21)
    title = models.TextField(max_length=500)
    description = models.TextField(max_length=10000, blank=True)
    date_start = models.DateField()
    date_stop = models.DateField()
    begin = models.IntegerField()
    end = models.IntegerField()
    # created = models.DateTimeField(editable=False)
    # modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        start = f"{datetime.date(int(self.start[0:4]), int(self.start[4:6]), int(self.start[6:8]))}"
        stop = f"{datetime.date(int(self.stop[0:4]), int(self.stop[4:6]), int(self.stop[6:8]))}"
        start_for_unix = datetime.datetime(int(self.start[0:4]),
                                           int(self.start[4:6]),
                                           int(self.start[6:8]),
                                           int(self.start[8:10]),
                                           int(self.start[10:12]),
                                           ).strftime('%s')
        stop_for_unix = datetime.datetime(int(self.stop[0:4]),
                                          int(self.stop[4:6]),
                                          int(self.stop[6:8]),
                                          int(self.stop[8:10]),
                                          int(self.stop[10:12]),
                                          ).strftime('%s')
        self.date_start = start
        self.date_stop = stop
        self.begin = start_for_unix
        self.end = stop_for_unix
        # if not self.id:
        #     self.created = timezone.now()
        # self.modified = timezone.now()
        return super(ProgrammeModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class TokenModel(models.Model):
    class Meta:
        db_table = 'token'
        ordering = ['id']
        verbose_name_plural = 'Сервис'

    name_service = models.CharField(max_length=40)
    token = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name_service} {self.token}'


class ChannelTokenModel(models.Model):
    class Meta:
        db_table = 'channel_token'
        ordering = ('token',)
        verbose_name_plural = 'Сервис - Каналы'

    token = models.ForeignKey(TokenModel, on_delete=models.CASCADE)
    day = models.IntegerField(default=1)
    date_select = models.IntegerField(blank=True, editable=False)
    channel = models.ManyToManyField(ChannelModel)

    def save(self, *args, **kwargs):
        self.date_select = self.day * 86400
        return super(ChannelTokenModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.token} {self.day}'

    def get_channel(self):
        return "\n".join([p.name for p in self.channel.all()])
