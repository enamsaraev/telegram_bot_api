import datetime
import pytz

from dataclasses import dataclass
from typing import Any, NamedTuple

from core.models import Category


class ParsedData(NamedTuple):
    amount: str
    expense: str


@dataclass
class UserID:
    id: int = 0

    def set_user_chat_id(self, id: int) -> None:
        """Set sender id"""

        self.id = id

    def get_user_chat_id(self) -> int:
        """Retrieving a sender id"""

        return self.id
    

@dataclass
class ParseText:
    text: str

    def __call__(self, *args: Any, **kwds: Any) -> None:
        
        return self._parse_text()

    def _parse_text(self) -> ParsedData or None:
        """Parsing input data"""

        data = self.text.split(' ')

        if len(data) != 2:
            return None
        
        if isinstance(int(data[0]), int) and isinstance(data[1], str):
            """Check id data is like <1500 coffee>"""
            
            return ParsedData(amount=data[0], expense=data[1])
        
        return None
    

@dataclass
class CategoryData:
    expense_text: str
    category: Category

    def __call__(self, *args: Any, **kwds: Any) -> dict:
        
        return {
            'amount': self._parse_text().amount,
            'created': self._get_now_formatted(),
            'category': self.category,
            'expense_text': self.expense_text,
        }

    def _get_now_formatted(self) -> str:
        """Return string datetime.now"""
        return self._get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")

    def _get_now_datetime(self) -> datetime.datetime:
        """Retruvncurrent msw datetime"""

        tz = pytz.timezone("Europe/Moscow")
        now = datetime.datetime.now(tz)

        return now
    
    def _parse_text(self) -> ParsedData:

        return ParseText(text=self.expense_text)()