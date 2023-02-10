import pytest

from mixer.backend.django import mixer

from core.models import (
    Expense, Category
)
from telegram_message_api.managers import (
    ExpenseManager, CategoryManager
)


@pytest.fixture()
def category(db):
    return mixer.blend('core.category', name='test', aliases='test, cafe, taxi')


def test_categorymanager_get_category_method(category):
    """Testing a CategoryManager get_category method"""

    mixer.cycle(5).blend('core.category')
    res = CategoryManager().get_category_by_aliases('test')

    assert res.aliases == category.aliases


def test_expensemanager_add_data_method(category):
    """Testing ExpenseManager add_data method"""

    CategoryManager().add_data(codename='codename', aliases='code, name')
    res = Category.objects.last()

    assert res.codename == 'codename'
    assert res.aliases == 'code, name'


def test_expensemanager_add_data_method(category):
    """Testing ExpenseManager add_data method"""

    ExpenseManager().add_data(text='150 test')
    res = Expense.objects.last()

    assert res.amount == 150
    assert res.expense_text == '150 test'
    assert res.category.name == 'test'

