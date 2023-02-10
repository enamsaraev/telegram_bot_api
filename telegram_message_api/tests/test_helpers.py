import pytest
import datetime
import pytz

from mixer.backend.django import mixer

from telegram_message_api.helpers import (
    ParsedData, ParseText, CategoryData,
)


@pytest.mark.parametrize(
    'text', [
        '150 test',
        '150 test 150',
        '150',
    ]
)
def test_parsetext_dataclass(text):
    """Testing a ParseText parse text method"""

    result = ParseText(text)()

    if result:
        assert result.amount == '150'
        assert result.expense == 'test'
    else:
        assert result == None


def test_categorydata_dataclass(db):
    """Testing a CategoryData"""

    category = mixer.blend('core.category')
    result = CategoryData(
        expense_text='150 test',
        category=category
    )()

    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    assert result == {
                        'amount': '150',
                        'created': now,
                        'category': category,
                        'expense_text': '150 test',
                     }