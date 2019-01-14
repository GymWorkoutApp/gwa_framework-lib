import base64
import calendar
import multiprocessing
from datetime import datetime, date, timedelta

from pytz import timezone
from schematics.exceptions import ValidationError

from gwap_framework.schemas.base import BaseSchema
from gwap_framework.schemas.pub_sub import PubSubMessage


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def pub_sub_message(schemma: BaseSchema, operation: str) -> PubSubMessage:
    message = PubSubMessage()
    message.message = schemma
    message.operation = operation
    return message


def get_cache_time() -> int:
    """
    Define cache time based in how many seconds are remaining between now and midnight
    :return: Integer
    """
    today = datetime.today().date().isoformat()
    brazil_timezone = timezone('America/Sao_Paulo')
    end_day = datetime.strptime(f'{today}T23:59:59.999999-0300', '%Y-%m-%dT%H:%M:%S.%f%z')
    now = datetime.now(tz=brazil_timezone)
    cache_seconds = (end_day - now).seconds
    return cache_seconds


def is_not_null(value):
    if value:
        return value
    raise ValidationError('Value must be informed')


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def base64_encode(value: str) -> bytes:
    return base64.b64encode(bytes(value, 'utf-8'))


def base64_decode(value: str) -> bytes:
    return base64.b64decode(bytes(value, 'utf-8'))


def sanitize_html_data(html_text: 'Tag') -> str:
    return html_text.text.replace('\n', '').replace('  ', '').strip()


def get_digit_only(text: str) -> str:
    return ''.join([x for x in text if x.isdigit()])


def get_only_upper(text: str) -> str:
    return ''.join([x for x in text if x.isupper()])


def check_weekday(date: datetime) -> bool:
    return date.weekday() in [5, 6]


def get_weekday(date: datetime) -> datetime:
    while check_weekday(date):
        date = date + timedelta(days=1)
    return date
