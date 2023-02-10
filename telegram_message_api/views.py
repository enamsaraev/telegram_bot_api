from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from telegram_message_api.managers import (
    ExpenseManager, CategoryManager
)


class BaseCategory(APIView):

    def get(self, request, *args, **kwargs):
        """Return all categories from db"""

        data = CategoryManager().get_current_categories()

        return Response({'msg': [data]}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Add an category to the db"""

        messege_category = request.data['category']
        messege_aliases = request.data['category_aliases']
        
        CategoryManager().add_data(
            codename=messege_category,
            aliases=messege_aliases
        )

        return Response({'msg': 'Категория сохранена'}, status=status.HTTP_200_OK)

class BaseExpense(APIView):

    def post(self, request, *args, **kwargs):
        """Add an expense to the db"""

        messege_text = request.data['msg_text']
        ExpenseManager().add_data(text=messege_text)

        return Response({'msg': 'Запись сохранена'}, status=status.HTTP_200_OK)
        
