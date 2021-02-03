# coding: utf-8

import sys
import os
import ctypes
from pathlib import Path
from PIL import Image
from bookworm import typehints as t
from bookworm.i18n import LocaleInfo
from bookworm.paths import data_path
from bookworm.ocr_engines import OcrRequest, OcrResult, BaseOcrEngine
from bookworm.logger import logger


log = logger.getChild(__name__)


class TesseractOcrEngine(BaseOcrEngine):
    name = "tesseract_ocr"
    display_name = _("Tesseract OCR Engine")
    _libtesseract = None

    @staticmethod
    def _check_on_windows():
        tesseract_lib_path = data_path("tesseract_ocr").resolve()
        if tesseract_lib_path.exists():
            ctypes.windll.kernel32.AddDllDirectory(str(tesseract_lib_path))
            os.environ["TESSDATA_PREFIX"] = str(tesseract_lib_path / "tessdata")
            return True
        return False

    @classmethod
    def check(cls) -> bool:
        if sys.platform == "win32" and not cls._check_on_windows():
            return False
        from . import pyocr
        cls._libtesseract = pyocr.libtesseract
        return cls._libtesseract.is_available()

    @classmethod
    def get_recognition_languages(cls) -> t.List[LocaleInfo]:
        langs = []
        for lng in cls._libtesseract.get_available_languages():
            try:
                langs.append(LocaleInfo.from_three_letter_code(lng))
            except ValueError:
                continue
        return langs

    @classmethod
    def recognize(cls, ocr_request: OcrRequest) -> OcrResult:
        img = Image.frombytes(
            "RGBA",
            (ocr_request.width, ocr_request.height),
            ocr_request.imagedata
        )
        recognized_text = cls._libtesseract.image_to_string(img, ocr_request.language.given_locale_name)
        return OcrResult(
            recognized_text=recognized_text,
            cookie=ocr_request.cookie,
        )
