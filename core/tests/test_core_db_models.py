import pytest

from mixer.backend.django import mixer

from core.models import (
    Budjet, Category, Expense
)


def test_successful_models_creation(db):
    """Test successful db models creation"""

    res = mixer.blend('core.category', name='test')

    assert res.name == 'test'