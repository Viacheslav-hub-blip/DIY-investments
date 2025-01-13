import time
import datetime
import undetected_chromedriver as uc
from undetected_chromedriver import By
from typing import NamedTuple
from webdriver_manager.chrome import ChromeDriverManager  # <- add


class Page(NamedTuple):
    link: str
    content: str


class ChromeParser:
    '''создание драйвера'''
    driver: uc.Chrome

    def __init__(self, options):
        self.driver = uc.Chrome(options=options)

    def _set_current_page(self, url: str):
        """Устанавливает текущую страницу"""
        self.driver.get(url)

    def _find_elements_by_class_name(self, class_names: [str]) -> [uc.webelement]:
        """Поиск элементов с определенными классами на текущей странице"""
        all_elements = []
        for class_name in class_names:
            try:
                elements = self.driver.find_elements(By.CLASS_NAME, class_name)
                all_elements += elements
            except:
                print('ошибка получения элемента по классу', class_name)
        return all_elements

    def _get_links_from_elements(self, elements: [uc.webelement]) -> list[str]:
        '''извлечение ссылок с текущей страницы'''
        links = []
        for element in elements:
            a_elements = element.children("a")
            for a_element in a_elements:
                links.append(a_element.get_attribute('href'))
        return list(set(links))

    def _get_content_from_page(self, page_link: list[str], elements_class_names: list[str]) -> list[Page]:
        '''извлечение содержимого с текушей страницы'''
        pages: list[Page] = []
        for link in page_link:
            self._set_current_page(link)
            div_elements = self._find_elements_by_class_name(elements_class_names)
            content = []
            for element in div_elements:
                content.append(element.text)
            pages.append(Page(link, "".join(content)))
            time.sleep(3)  # задержка между переходами на страницы для повышения незаметности
        return pages

    def get_content_with_link(self, base_url: str, elements_with_links_class_name: list[str],
                              elements_names_with_content: list[str], max_pages: int) -> list[Page]:
        """Возвращает собранный текст и ссылку и на источник"""
        self._set_current_page(base_url)
        elements_with_links_on_base_page = self._find_elements_by_class_name(elements_with_links_class_name)
        links_on_base_page: list[str] = self._get_links_from_elements(elements_with_links_on_base_page[:max_pages])
        pages_with_content = self._get_content_from_page(links_on_base_page, elements_names_with_content)
        self.driver.quit()
        return pages_with_content


if __name__ == '__main__':
    options = uc.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_parser = ChromeParser(options)
    pages = chrome_parser.get_content_with_link('https://www.bloomberg.com/search?query=Tesla',
                                                ['thumbnailWrapper__23c201ad78'],
                                                ['media-ui-Paragraph_text-SqIsdNjh0t0-',
                                                 'media-ui-Paragraph_text-SqIsdNjh0t0- paywall',
                                                 'media-ui-HedAndDek_headline-D19MOidHYLI-',
                                                 'media-ui-Timestamp_timestampWrapper-w-YevWapP-k-', ],
                                                3)
