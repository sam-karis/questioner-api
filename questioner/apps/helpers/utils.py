from django.utils.timezone import get_current_timezone
from datetime import datetime
from rest_framework import serializers


class ConvertDate(object):

    def convert_date(self, str_date):
        if str_date is None:
            raise serializers.ValidationError(
                'Start_time and end_time must be provided.'
            )
        tz = get_current_timezone()
        try:
            date = tz.localize(datetime.strptime(str_date, '%Y-%m-%d%H:%M'))
            return date
        except ValueError as e:
            raise serializers.ValidationError(
                str(e)
            )
