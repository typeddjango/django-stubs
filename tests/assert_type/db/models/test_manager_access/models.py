"""Managers are only accessible on the model class, never on an instance of that model.

Django only imports this module, so every model from the sibling use-case modules is re-exported here.
"""

from __future__ import annotations

from .drf_like import CategoryHolder, QuerySetHolder, UnparametrizedHolder
from .objects import Category, CategoryManager, Post
from .protocol import PermissionAware
from .reverse_relations import Article, Node

__all__ = [
    "Article",
    "Category",
    "CategoryHolder",
    "CategoryManager",
    "Node",
    "PermissionAware",
    "Post",
    "QuerySetHolder",
    "UnparametrizedHolder",
]
