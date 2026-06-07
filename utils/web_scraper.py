"""
Web Scraper Utilities
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from loguru import logger
import asyncio
from urllib.parse import urljoin, urlparse
import time
import json


class WebScraper:
    """Web scraping utilities for market research"""
    
    def __init__(self, user_agent: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'AI-Agent-Ecosystem/1.0'
        })
        self.rate_limit_delay = 1  # seconds between requests
        
    def scrape_page(self, url: str) -> Optional[str]:
        """
        Scrape a single page
        
        Args:
            url: URL to scrape
            
        Returns:
            HTML content or None
        """
        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content
        
        Args:
            html: HTML string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'html.parser')
    
    def extract_text(self, soup: BeautifulSoup, selector: str = None) -> str:
        """
        Extract text from HTML
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector to extract from
            
        Returns:
            Extracted text
        """
        if selector:
            elements = soup.select(selector)
            return ' '.join([e.get_text(strip=True) for e in elements])
        
        return soup.get_text(strip=True)
    
    def extract_links(self, soup: BeautifulSoup, base_url: str = None) -> List[str]:
        """
        Extract all links from page
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for relative links
            
        Returns:
            List of absolute URLs
        """
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if base_url:
                href = urljoin(base_url, href)
            if href.startswith(('http://', 'https://')):
                links.append(href)
        return links
    
    def extract_structured_data(self, soup: BeautifulSoup) -> Dict:
        """
        Extract structured data (JSON-LD, meta tags, etc.)
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dictionary of structured data
        """
        data = {}
        
        # Extract JSON-LD
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                json_data = json.loads(script.string)
                if isinstance(json_data, dict):
                    data.update(json_data)
                elif isinstance(json_data, list):
                    for item in json_data:
                        if isinstance(item, dict):
                            data.update(item)
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Extract meta tags
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        
        if meta_tags:
            data['meta_tags'] = meta_tags
        
        return data
    
    async def scrape_multiple(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """
        Scrape multiple URLs concurrently
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            Dictionary of URL to HTML content
        """
        async def scrape_one(url):
            loop = asyncio.get_event_loop()
            return url, await loop.run_in_executor(None, self.scrape_page, url)
        
        tasks = [scrape_one(url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        return dict(results)
    
    def search_news(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search news for a query
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of news articles
        """
        # Note: This is a placeholder. In production, use News API or similar
        logger.info(f"Searching news for: {query}")
        
        # Example using Google News RSS (for demonstration)
        news_url = f"https://news.google.com/rss/search?q={query}"
        html = self.scrape_page(news_url)
        
        if not html:
            return []
        
        soup = self.parse_html(html)
        articles = []
        
        for item in soup.find_all('item')[:num_results]:
            articles.append({
                'title': item.find('title').get_text() if item.find('title') else '',
                'link': item.find('link').get_text() if item.find('link') else '',
                'description': item.find('description').get_text() if item.find('description') else '',
                'pub_date': item.find('pubDate').get_text() if item.find('pubDate') else ''
            })
        
        return articles
    
    def extract_company_info(self, domain: str) -> Dict:
        """
        Extract company information from website
        
        Args:
            domain: Company domain
            
        Returns:
            Company information dictionary
        """
        url = f"https://{domain}"
        html = self.scrape_page(url)
        
        if not html:
            return {}
        
        soup = self.parse_html(html)
        
        info = {
            'domain': domain,
            'title': soup.title.string if soup.title else '',
            'description': '',
            'keywords': '',
            'structured_data': self.extract_structured_data(soup)
        }
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            info['description'] = meta_desc.get('content', '')
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            info['keywords'] = meta_keywords.get('content', '')
        
        return info