import setuptools

VERSION = "0.0.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google_translator_simplified",
    version=VERSION,
    author="Kamila Sproska",
    author_email="kamila.sproska@gmail.com",
    description="Class for translating texts and detecting language (based on Google Translator).",
    long_description=long_description,
    keywords=['python', 'google', 'translator', 'simple', 'google translator'],
    url="https://github.com/ksproska/google_translator_simplified",
    packages=setuptools.find_packages()
)
