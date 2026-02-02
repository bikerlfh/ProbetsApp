import logging
from typing import Callable, Optional, Dict, Any, Union, List
# import chromedriver_binary  # noqa
from chromeless import chromeless
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from apps.third_parties.constants import USE_CHROMELESS


logger = logging.getLogger(__name__)


class ChromeCustom:
    def __init__(self, options: Optional[Options] = None):
        if not USE_CHROMELESS:
            if not options:
                options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("window-size=1400,1500")
            self._driver = webdriver.Chrome(options=options)
        else:
            self._driver = chromeless.Chromeless()
            self._driver.attach(get_content)
            self._driver.attach(get_content_by_xpath_click)
            self._driver.attach(exec_function)
            self._driver.attach(close)

    def get_content(
        self,
        url: str,
        wait_until_method: Optional[Callable] = None,
        wait_seconds: Optional[int] = 20,
        scroll: Optional[bool] = False
    ) -> str:
        if isinstance(self._driver, chromeless.Chromeless):
            return self._driver.get_content(
                url,
                wait_until_method=wait_until_method,
                wait_seconds=wait_seconds,
                scroll=scroll
            )
        self._driver.get(url)
        if wait_until_method:
            WebDriverWait(self._driver, wait_seconds).until(wait_until_method)
        if scroll:
            last_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            while True:
                self._driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                new_height = self._driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height
        return self._driver.page_source

    def get_content_by_xpath_click(
        self,
        url: str,
        xpath: str,
        wait_until_method: List[Callable],
        wait_seconds: Optional[int] = 90,
        scroll: Optional[bool] = False
    ) -> str:
        if isinstance(self._driver, chromeless.Chromeless):
            return self._driver.get_content_by_xpath_click(
                url,
                xpath,
                wait_until_method=wait_until_method,
                wait_seconds=wait_seconds,
                scroll=scroll
            )
        div_ods = self._driver.find_element_by_xpath(xpath)
        div_ods.click()
        WebDriverWait(self._driver, wait_seconds).until(wait_until_method[1])
        last_height = self._driver.execute_script(
            "return document.body.scrollHeight"
        )
        while True:
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            new_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
        return self._driver.page_source

    def find_element_by_xpath(self, xpath):
        return self._driver.find_element_by_xpath(xpath)

    def close(self):
        if isinstance(self._driver, chromeless.Chromeless):
            return
        self._driver.close()


def exec_function(
    self,
    func_name,
    params: Optional[Dict[str, Any]] = dict
) -> Union[Any, None]:
    func_ = getattr(self, func_name, None)
    if func_ is None:
        return
    return func_(**params)


def close(self):
    self.close()


def get_content(
    self,
    url: str,
    wait_until_method: Optional[Callable] = None,
    wait_seconds: Optional[int] = 90,
    scroll: Optional[bool] = False
) -> str:
    """
    Get page content of url
    """
    self.get(url)
    if wait_until_method:
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self, wait_seconds).until(wait_until_method)
    if scroll:
        last_height = self.execute_script(
            "return document.body.scrollHeight"
        )
        while True:
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            new_height = self.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
    return self.page_source


def get_content_by_xpath_click(
    self,
    url: str,
    xpath: str,
    wait_until_method: List[Callable],
    wait_seconds: Optional[int] = 90,
    scroll: Optional[bool] = False
) -> str:
    """
    Get page content of url
    """
    from selenium.webdriver.support.ui import WebDriverWait
    self.get(url)
    WebDriverWait(self, wait_seconds).until(wait_until_method[0])
    if scroll:
        last_height = self.execute_script(
            "return document.body.scrollHeight"
        )
        while True:
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            new_height = self.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
    element = self.find_element_by_xpath(xpath)
    element.click()
    WebDriverWait(self, 90).until(wait_until_method[1])
    if scroll:
        last_height = self.execute_script(
            "return document.body.scrollHeight"
        )
        while True:
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            new_height = self.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
    return self.page_source
