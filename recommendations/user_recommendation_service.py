from collections import Counter
from typing import Literal

from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

from catalog.models import Book
from recommendations.models.recommendation import Recommendation

User = get_user_model()


class RecommendationService:
    """Сервис рекомендаций"""
    def __init__(self, user: User):
        self.user = user

    def _get_user_books(self) -> QuerySet[Book]:
        """Получаем все книги которые есть в библиотеке пользователя"""
        return Book.objects.filter(library_item__user=self.user)

    def _get_user_preferences(self) -> dict[Literal['authors'] | Literal['genres'], Counter]:
        """Считаем, что чем чаще встречается автор/жанр, тем выше интерес"""
        books = self._get_user_books()
        author_counter = Counter()
        genre_counter = Counter()

        for book in books:
            for author in book.authors.all():
                author_counter[author] += 1
            for genre in book.genres.all():
                genre_counter[genre] += 1

        return {
            'authors': author_counter,
            'genres': genre_counter
        }

    def _get_similar_users(self, preferences: dict[Literal['authors'] | Literal['genres'], Counter]) -> QuerySet[User]:
        """Ищем пользователей с похожими предпочтениями"""
        authors = list(preferences['authors'].keys())
        genres = list(preferences['genres'].keys())

        users = User.objects.filter(
            Q(library_item__book__authors__in=authors) |
            Q(library_item__book__genres__in=genres)
        ).exclude(id=self.user.id).distinct()

        return users

    def _get_candidate_books(self, similar_users) -> QuerySet[Book]:
        """Берём книги похожих пользователей"""
        return Book.objects.filter(
            library_item__user__in=similar_users
        ).exclude(
            library_item__user=self.user  # исключаем уже прочитанные самим юзером
        ).distinct()

    def add_recommendations(self, limit: int = 50) -> None:
        """Добавляет рекомендованные для пользователя книги в базу данных"""
        preferences = self._get_user_preferences()
        similar_users = self._get_similar_users(preferences)
        candidates = self._get_candidate_books(similar_users)
        scored_books = []
        for book in candidates:
            score = 0
            for author in book.authors.all():
                score += preferences['authors'].get(author, 0) * 2
            for genre in book.genres.all():
                score += preferences['genres'].get(genre, 0)
            if score > 0:
                scored_books.append((book, score))
        Recommendation.objects.bulk_create(
            [Recommendation(user=self.user, book=book, score=score) for book, score in scored_books[:limit]]
        )
