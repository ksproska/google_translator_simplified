import json
import unittest
from .translator_complex import GoogleTranslator
from . import translator_constant as t_const


class Translator:
    """"
        Class for translating texts and detecting language (based on Google Translator).
    """
    TRANSLATOR = GoogleTranslator()
    DICTIONARY_ABBREVIATION = t_const.LANGUAGES
    DICTIONARY_NAMES = {v: k for k, v in DICTIONARY_ABBREVIATION.items()}
    MAX_DETECT_TEXT_LEN = 500  # necessary because for longer texts it throws exception

    class TranslatorUntranslatableError(ValueError):
        """
        Occurs when language is undetectable (for example for texts with just spaces).
        """

        def __init__(self, given_text: str, *args, **kwargs):
            self.given_text = given_text
            super().__init__(*args, **kwargs)

        def __str__(self):
            return f'Given text:\n"{self.given_text}"\n is untranslatable.'

    class TranslatorIncorrectAbbreviation(ValueError):
        """
        Occurs when language abbreviation is not correct.
        """

        def __init__(self, given_abbreviation: str, *args, **kwargs):
            self.given_abbreviation = given_abbreviation
            super().__init__(*args, **kwargs)

        def __str__(self):
            return f'Given abbreviation: "{self.given_abbreviation}" is not correct.\nCorrect abbreviations: {Translator.abbreviation_list}'

    class TranslatorConnectionError(ConnectionError):
        """
        Occurs when Translator couldn't connect to the Internet.
        """

        def __str__(self):
            return f'Couldn\'t connect to the Internet.'

    @classmethod
    def get_translation(cls, destination_lang: str, text: str, source_lang: str = None):
        """
        Returns translated text in destination_language. If source_language is not given, language is detected.
        Languages are expected in a form of abbreviation: e.g. en, de, pl

        :param text: text for language translation
        :param source_lang: language (in a form of abbreviation) of text, if None - language detected
        :param destination_lang: language (in a form of abbreviation) of expected translation
        :return: translated text in destination_lang
        """
        if destination_lang not in cls.abbreviation_list:
            raise cls.TranslatorIncorrectAbbreviation(destination_lang)
        try:
            if source_lang is None:
                source_lang = cls.detect_lang(text)
            elif source_lang not in cls.abbreviation_list:
                raise cls.TranslatorIncorrectAbbreviation(source_lang)
            return cls.TRANSLATOR.translate(text, lang_src=source_lang, lang_tgt=destination_lang)
        except json.decoder.JSONDecodeError:
            cls.TranslatorUntranslatableError(text)
        except Exception as e:
            if e.__str__() == 'Failed to connect. Probable cause: timeout':
                raise cls.TranslatorConnectionError()
            raise e

    @classmethod
    def detect_lang(cls, text: str) -> str:
        """
        Detects language of given text and returns it in a form of abbreviation, e.g. en, de, pl

        :param text: text for language detection
        :return: language (in a form of abbreviation)
        """
        try:
            if len(text) >= cls.MAX_DETECT_TEXT_LEN:
                text = text[:cls.MAX_DETECT_TEXT_LEN - 1]
            detect_result = cls.TRANSLATOR.detect(text)
            if detect_result[0] == 'zh-CN':
                raise cls.TranslatorUntranslatableError(text)
            return detect_result[0]
        except Exception as e:
            if e.__str__() == 'Failed to connect. Probable cause: timeout':
                raise cls.TranslatorConnectionError()
            raise cls.TranslatorUntranslatableError(text)

    @classmethod
    @property
    def names_list(cls) -> list:
        """
        List of languages' full names (in alphabetical order), ['afrikaans', 'albanian', 'amharic', 'arabic',...]
        """
        return list(cls.DICTIONARY_NAMES.keys())

    @classmethod
    @property
    def abbreviation_list(cls) -> list:
        """
        List of languages' abbreviations in order of languages' full names list, ['af', 'sq', 'am', 'ar',...]
        """
        return list(cls.DICTIONARY_ABBREVIATION.keys())

    @classmethod
    def get_abbreviation(cls, name: str):
        """
        :param name: Language full name, e.g. english, german, polish
        :return: Language abbreviation, e.g. en, de, pl
        """
        if name not in cls.DICTIONARY_NAMES:
            return None
        return cls.DICTIONARY_NAMES[name]

    @classmethod
    def get_name(cls, abbreviation: str):
        """
        :param abbreviation: Language abbreviation, e.g. en, de, pl
        :return: Language full name, e.g. english, german, polish
        """
        if abbreviation not in cls.DICTIONARY_ABBREVIATION:
            return None
        return cls.DICTIONARY_ABBREVIATION[abbreviation]


class TestTranslator(unittest.TestCase):
    def test_get_translation(self):
        self.assertEqual(Translator.get_translation('pl', 'text for translation', 'en'), 'Tekst do tłumaczenia ')
        self.assertEqual(Translator.get_translation('de', 'tekst do przetłumaczenia', 'pl'), 'Text für die Übersetzung ')
        self.assertEqual(Translator.get_translation('pl', 'text for translation'), 'Tekst do tłumaczenia ')
        self.assertEqual(Translator.get_translation('de', 'tekst do przetłumaczenia'), 'Text für die Übersetzung ')

    def test_detect_lang(self):
        self.assertEqual(Translator.detect_lang('text for translation'), 'en')
        self.assertEqual(Translator.detect_lang('Mittwoch'), 'de')
        self.assertEqual(Translator.detect_lang('inny przykład'), 'pl')

    def test_get_abbreviation(self):
        self.assertEqual(Translator.get_abbreviation('english'), 'en')
        self.assertEqual(Translator.get_abbreviation('polish'), 'pl')
        self.assertEqual(Translator.get_abbreviation('german'), 'de')

    def test_get_name(self):
        self.assertEqual(Translator.get_name('en'), 'english')
        self.assertEqual(Translator.get_name('pl'), 'polish')
        self.assertEqual(Translator.get_name('de'), 'german')

    def test_names_list(self):
        self.assertEqual(Translator.names_list[:7], ['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque'])
        self.assertEqual('english' in Translator.names_list, True)
        self.assertEqual('german' in Translator.names_list, True)
        self.assertEqual('polish' in Translator.names_list, True)

    def test_abbreviation_list(self):
        self.assertEqual(Translator.abbreviation_list[:7], ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu'])
        self.assertEqual('en' in Translator.abbreviation_list, True)
        self.assertEqual('de' in Translator.abbreviation_list, True)
        self.assertEqual('pl' in Translator.abbreviation_list, True)

    def test_untranslatableError(self):
        self.assertRaises(Translator.TranslatorUntranslatableError, Translator.detect_lang, '')
        self.assertRaises(Translator.TranslatorUntranslatableError, Translator.detect_lang, '``2564&&')
        self.assertRaises(Translator.TranslatorUntranslatableError, Translator.detect_lang, '   ')
        self.assertRaises(Translator.TranslatorUntranslatableError, Translator.detect_lang, ' \t\n')

    def test_IncorrectAbbreviation(self):
        self.assertRaises(Translator.TranslatorIncorrectAbbreviation, Translator.get_translation, '', 'text for translation')
        self.assertRaises(Translator.TranslatorIncorrectAbbreviation, Translator.get_translation, 'd', 'text for translation')
        self.assertRaises(Translator.TranslatorIncorrectAbbreviation, Translator.get_translation, 'de', 'text for translation', 'e')
