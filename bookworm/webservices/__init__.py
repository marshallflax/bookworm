# coding: utf-8

import wx
from bookworm.base_service import BookwormService
from bookworm.logger import logger
from .wikiworm import WikipediaService
from .url_open import UrlOpenService


log = logger.getChild(__name__)


class WebservicesBaseService(BookwormService):
    name = "webservices"
    has_gui = True

    def __post_init__(self):
        self.web_sservices_menu = wx.Menu()

    def process_menubar(self, menubar):
        self.view.menuBar.Insert(3, self.web_sservices_menu, _("&Web Services"))
