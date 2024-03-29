from abc import ABC, abstractmethod
from typing import List
from django.contrib.auth import get_user_model
from core.models import (
    Budjet, Category, Expense
)
from telegram_message_api.helpers import ParseText, CategoryData


class DBManager(ABC):

    @abstractmethod
    def add_data(self, *args, **kwargs):
        pass


class CategoryManager(DBManager):

    def __init__(self, chat_id: int) -> None:
        self._chat_id = chat_id
        self._categories = self._get_all_categories()
        self._list_of_categories_for_user = self._normalize_categories()

    def _get_all_categories(self) -> List[Category]:
        """Return all current categories from db"""

        return Category.objects.select_related(
            'user'
        ).filter(user=get_user_model().objects.get(chat_id=self._chat_id))
    
    def _normalize_categories(self) -> dict:
        """Normalize category data for user"""
        
        data = {}
        for category in self._categories:
            data[category.codename] = category.aliases

        return data

    def add_data(self, codename: str, aliases: str) -> Category:
        
        Category.objects.create(
            user=get_user_model().objects.get(chat_id=self._chat_id),
            codename=codename,
            aliases=aliases
        )

    def get_category_by_aliases(self, expense_text: str) -> Category:
        """Retrieving a category by matching expense_text with category aliases"""

        other_category = None

        for category in self._categories:
            if category.name == 'Else':
                other_category = category
            if expense_text in category.aliases:
                return category
            
        return other_category
    
    def get_current_categories(self):

        return self._list_of_categories_for_user


class ExpenseManager(DBManager):

    def __init__(self, chat_id) -> None:
        self._chat_id = chat_id

    def add_data(self, text: str) -> None:
        """Adding expense to the db"""

        parsed_text = ParseText(text=text)()
        category = CategoryManager(chat_id=self._chat_id).get_category_by_aliases(parsed_text.expense)
        print(category.codename, category.name)
        data = CategoryData(
            category=category,
            expense_text=text
        )()

        Expense.objects.create(
            user=get_user_model().objects.get(chat_id=self._chat_id),
            category=data['category'],
            amount=int(data['amount']),
            created_date=data['created'],
            expense_text=data['expense_text']
        )

        
