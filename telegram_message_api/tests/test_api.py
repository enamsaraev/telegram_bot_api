import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from core.models import Expense, Category


@pytest.fixture
def user(db):
    """Test user with chat_id"""

    user = mixer.blend(
        get_user_model(),
        email='shaufau@mail.com',
        password='shaufau174',
        chat_id=5678914,
    )
    return user

def test_adding_an_expense(db, user, api):
    """
        Test BAseManager post view: 
        adding information about current expense
    """
    mixer.blend(Category, aliases='test', user=user)
    response_data = {
        'user_chat_id': user.chat_id,
        'msg_text': '150 test',
    }
    response = api.post(reverse('telegram_message_api:add_expense'), data=response_data)
    assert response.status_code == 200

    last_expense = Expense.objects.last()
    assert last_expense.expense_text == response_data['msg_text']


def test_adding_an_category(db, user, api):
    """
        Test BAseManager post view: 
        adding information about current expense
    """
    response_data = {
        'user_chat_id': user.chat_id,
        'category': 'category',
        'category_aliases': 'some, aliases',
    }
    response = api.post(reverse('telegram_message_api:add_category'), data=response_data)
    assert response.status_code == 200

    last_category = Category.objects.last()
    assert last_category.codename == response_data['category']


def test_user_authenticate(db, user, api):
    """Testing user model creation or authentication"""

    response_data = dict(
        user_email=user.email,
        user_password=user.password,
        user_chat_id=user.chat_id,
    )

    res = api.post(reverse('telegram_message_api:user_registration'), data=response_data)
    assert res.status_code == 200


def test_user_registration(db, user, api):
    """Testing user model creation or authentication"""

    response_data = dict(
        user_email=user.email,
        user_password=user.password,
        user_chat_id=user.chat_id,
    )

    res = api.post(reverse('telegram_message_api:user_registration'), data=response_data)
    assert res.status_code == 200