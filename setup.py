import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'HISTORY.rst')).read()

requires = [
    'pyramid',
    'rawes>=0.5.4'
    ]

setup(
    name='pyramid_rawes',
    version='0.5.1',
    license='MIT',
    description='Rawes bindings for pyramid',
    long_description=README + '\n\n' +  CHANGES,
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
    ],
    author='Koen Van Daele',
    author_email='koen_van_daele@telenet.be',
    url='https://github.com/koenedaele/pyramid_rawes',
    keywords='pyramid elastic search rawes',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = requires,
    test_suite='pyramid_rawes',
)
