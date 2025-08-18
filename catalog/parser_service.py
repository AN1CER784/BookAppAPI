import asyncio
import logging
from typing import Optional, Union

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36',
}


class ParserService:
    """Сервис для парсинга флибусты"""
    def __init__(self):
        self.site = "https://flibusta.is"
        logger.debug(f"Initialized parser with site={self.site}")

    @staticmethod
    async def get_html_with_retry(session: aiohttp.ClientSession, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Асинхронно получает HTML с повторными попытками
        """
        logger.info(f"Fetching URL: {url} with up to {max_retries} retries")
        for attempt in range(1, max_retries + 1):
            try:
                logger.debug(f"Attempt {attempt} for {url}")
                async with session.get(url, headers=header) as resp:
                    resp.raise_for_status()
                    text = await resp.text()
                    logger.info(f"Successfully fetched {url} (length={len(text)})")
                    return text
            except Exception as e:
                logger.warning(f"Error fetching URL (attempt {attempt}): {e}")
                await asyncio.sleep(1)
        logger.error(f"Failed to fetch URL after {max_retries} attempts: {url}")
        return None

    async def get_books(
        self, html: str, page: bool = False
    ) -> Union[list[str], list[tuple[str, list[str], list[str], list[str], str]]]:
        """
        Парсит HTML и возвращает книги
        """
        logger.info(f"Parsing HTML for catalog (page_mode={page})")
        result = []
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find("div", id="main")
        if not div:
            logger.error("Main div not found in HTML")
            return result
        if page:
            title = soup.find("h1", class_="title").text if soup.find("h1", class_="title") else "[No title]"
            logger.debug(f"Page title: {title}")
            try:
                links = div.find_all("a")
                books = [self.site + link['href'] for link in links
                         if link.get('href', '').startswith("/b/") and not link['href'].endswith("/read")]
                logger.debug(f"Found {len(books)} book links on page")
            except KeyError:
                logger.error("KeyError when extracting book hrefs")
                return []
            authors_tags = div.find_all("a", href=lambda href: href and href.startswith("/a/"))
            authors = [a.text for a in authors_tags][1:]
            genres = [a.text for a in div.find_all("a", href=lambda href: href and href.startswith("/g/"))]
            logger.debug(f"Found {len(authors)} authors: {authors}")
            logger.debug(f"Found {len(genres)} genres: {genres}")
            annotation_ps = div.find_all("p", class_=None)
            annotation = annotation_ps[0].text if len(annotation_ps) > 1 else "No annotation"
            logger.debug(f"Annotation: {annotation[:100]}...")
            result.append((title, authors, genres, books, annotation))
        else:
            items = div.find_all('li')
            urls = [a.get('href') for li in items for a in li.find_all('a')]
            books_url = [self.site + href for href in urls if href and href.startswith("/b/")][:1000]
            logger.debug(f"Found {len(books_url)} book URLs in list")
            result.extend(books_url)
        return result

    async def get_book_links(self, session: aiohttp.ClientSession, links: list[str]) -> list[
        tuple[str, list[str], list[str], list[str], str]]:
        """
        Получает детальную информацию о книгах по списку ссылок
        """
        logger.info(f"Getting detailed book info for {len(links)} links")
        result = []
        for idx, link in enumerate(links, start=1):
            logger.debug(f"Fetching book detail {idx}/{len(links)}: {link}")
            html = await self.get_html_with_retry(session, link)
            if html:
                books = await self.get_books(html, page=True)
                logger.debug(f"Parsed {len(books)} entries from {link}")
                result.extend(books)
            else:
                logger.warning(f"Skipping link due to fetch failure: {link}")
        return result

    async def parsing(self, session: aiohttp.ClientSession) -> Union[
        str, list[tuple[str, list[str], list[str], list[str], str]]]:
        """
        Полный процесс парсинга
        """
        logger.info("Starting full parsing process")
        start_url = f"{self.site}/stat/b"
        html = await self.get_html_with_retry(session, start_url)
        if not html:
            logger.error("Error fetching start page HTML")
            return "Error fetching HTML"
        books_list = await self.get_books(html)
        if not books_list:
            logger.warning("No catalog found on start page")
            return "The book not found!"
        logger.info(f"Found {len(books_list)} book links on start page")
        result = await self.get_book_links(session, books_list)
        logger.info(f"Completed parsing, total catalog parsed: {len(result)}")
        return result
