import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'HISTORY.rst')).read()

requires = [
    'pyramid',
    'rawes'
    ]

tests_requires = []

testing_extras = tests_requires + [
    'nose',
    'coverage'
    ]

setup(name='pyramid_rawes',
      version='0.1.0',
      license='MIT',
      description='RawES binding for pyramid',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        "Framework :: Pyramid",
        ],
      author='Koen Van Daele',
      author_email='koen_van_daele@telenet.be',
      url='',
      keywords='pyramid elastic search rawes',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require = tests_requires,
      extras_require = {
        'testing': testing_extras
        },
      test_suite='pyramid_rawes',
      )
