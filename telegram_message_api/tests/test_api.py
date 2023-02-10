import pytest

from django.urls import reverse
from mixer.backend.django import mixer

from core.models import Expense, Category


def test_adding_an_expense(db, api):
    """
        Test BAseManager post view: 
        adding information about current expense
    """
    mixer.blend(Category, aliases='test')
    response_data = {
        'msg_text': '150 test',
    }
    response = api.post(reverse('telegram_message_api:add_expense'), data=response_data)
    assert response.status_code == 200

    last_expense = Expense.objects.last()
    assert last_expense.expense_text == response_data['msg_text']


def test_adding_an_category(db, api):
    """
        Test BAseManager post view: 
        adding information about current expense
    """
    response_data = {
        'category': 'category',
        'category_aliases': 'some, aliases',
    }
    response = api.post(reverse('telegram_message_api:add_category'), data=response_data)
    assert response.status_code == 200

    last_category = Category.objects.last()
    assert last_category.codename == response_data['category']
