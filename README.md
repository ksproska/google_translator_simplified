Class for translating texts and detecting language (based on Google Translator).

```python
from google_translator_simplified import Translator
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
```