import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(name='traffic',
    version='0.1.0',
    description='Download and clean Schiphol traffic data',
    long_description=README,
    long_description_content_type="text/markdown",
    author='dirkmjk',
    author_email='info@dirkmjk.nl',
    license="MIT",
    packages=['traffic'],
    install_requires=['pandas', 'requests', 'BeautifulSoup'],
    zip_safe=False)
