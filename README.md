Class for translating texts and detecting language (based on Google Translator).

Get text translation:
```python
from google_translator_simplified import Translator

Translator.get_translation('pl', 'text for translation', 'en') #'Tekst do tłumaczenia '
Translator.get_translation('de', 'tekst do przetłumaczenia', 'pl') #'Text für die Übersetzung '
Translator.get_translation('pl', 'text for translation') #'Tekst do tłumaczenia '
Translator.get_translation('de', 'tekst do przetłumaczenia') #'Text für die Übersetzung '
```
Detect language:
```python
from google_translator_simplified import Translator

Translator.detect_lang('text for translation') #'en'
Translator.detect_lang('Mittwoch') #'de'
Translator.detect_lang('inny przykład') #'pl'
```
Get language abbreviation:
```python
from google_translator_simplified import Translator

Translator.get_abbreviation('english') #'en'
Translator.get_abbreviation('polish') #'pl'
Translator.get_abbreviation('german') #'de'
```
Get language full name:
```python
from google_translator_simplified import Translator

Translator.get_name('en') #'english'
Translator.get_name('pl') #'polish'
Translator.get_name('de') #'german'
```
names list:
```python
from google_translator_simplified import Translator

Translator.names_list[:7] #['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque'])
```
abbreviation list:
```python
from google_translator_simplified import Translator

Translator.abbreviation_list[:7] #['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu']
```
Errors:
```python
from google_translator_simplified import Translator
import unittest
class TestTranslator(unittest.TestCase):
    def test_untranslatableError(self):
        self.assertRaises(Translator.TranslatorUntranslatableError, 
                          Translator.detect_lang, '')
        self.assertRaises(Translator.TranslatorUntranslatableError, 
                          Translator.detect_lang, '``2564&&')
        self.assertRaises(Translator.TranslatorUntranslatableError, 
                          Translator.detect_lang, '   ')
        self.assertRaises(Translator.TranslatorUntranslatableError, 
                          Translator.detect_lang, ' \t\n')
    
    def test_IncorrectAbbreviation(self):
        self.assertRaises(Translator.TranslatorIncorrectAbbreviation, 
                          Translator.get_translation, '', 'text for translation')
        self.assertRaises(Translator.TranslatorIncorrectAbbreviation, 
                          Translator.get_translation, 'd', 'text for translation')
        self.assertRaises(Translator.TranslatorIncorrectAbbreviation, 
                          Translator.get_translation, 'de', 'text for translation', 'e')
```