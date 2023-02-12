import pytest

from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from core.models import (
    Expense, Category
)
from telegram_message_api.managers import (
    ExpenseManager, CategoryManager
)


@pytest.fixture()
def user(db):
    user = mixer.blend(get_user_model())
    return user


@pytest.fixture()
def category(db, user):
    return mixer.blend('core.category', user=user, name='test', aliases='test, cafe, taxi')


def test_categorymanager_get_category_method(user, category):
    """Testing a CategoryManager get_category method"""

    mixer.cycle(5).blend('core.category', user=mixer.blend(get_user_model(), chat_id=1234567))
    res = CategoryManager(chat_id=user.chat_id).get_category_by_aliases('test')

    assert res.aliases == category.aliases


def test_expensemanager_add_data_method(category):
    """Testing ExpenseManager add_data method"""

    CategoryManager().add_data(codename='codename', aliases='code, name')
    res = Category.objects.last()

    assert res.codename == 'codename'
    assert res.aliases == 'code, name'


def test_expensemanager_add_data_method(user, category):
    """Testing ExpenseManager add_data method"""

    ExpenseManager(user.chat_id).add_data(text='150 test')
    res = Expense.objects.last()

    assert res.amount == 150
    assert res.expense_text == '150 test'
    assert res.category.name == 'test'
    assert res.user == user
