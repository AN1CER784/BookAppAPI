import asyncio

import aiohttp
from django.core.management import BaseCommand
from catalog.parser_service import ParserService
from catalog.api.serializers import BookCreateSerializer
from catalog.utils import serializer_save


class Command(BaseCommand):
    help = 'Parses book data on book name'

    def handle(self, *args, **options):
        asyncio.run(self.run_parser())

    async def run_parser(self):
        parser = ParserService()
        async with aiohttp.ClientSession() as session:
            books = await parser.parsing(session)
            for book in books:
                book_name, authors, genres, links, description = book
                book_links = list(filter(lambda link: link.endswith(("fb2", "epub", "mobi")), links))
                if not book_links or not authors or not genres:
                    continue
                book_data = {
                    "name": book_name,
                    "description": description,
                    "authors": [{"name": author} for author in authors],
                    "genres": [{"name": genre} for genre in genres],
                    "book_links": [{"link": link} for link in book_links]
                }
                book_serializer = BookCreateSerializer(data=book_data)
                await serializer_save(book_serializer)
