from setuptools import setup
from codecs import open
from os import path
from warnings import warn

def readme():
    here = path.abspath(path.dirname(__file__))
    readme = path.join(here, 'README.md')
    
    try:
        import pypandoc
        long_description = pypandoc.convert_file(readme, 'rst', format='md')
    except ImportError:
        warn("Markdown -> Rst convestion failed")
        with open(readme, encoding='utf-8') as f:
            long_description = f.read()
            
    return long_description

setup(name='kobato',
      version='0.1',
      description='A command line interface to your point.im blog',
      long_description=readme(),
      url='https://github.com/nico-izo/kobato',
      author='Nicolay Izoderov',
      author_email='nico-izo@ya.ru',
      license='GNU/GPLv3',
      packages=['kobato'],
      install_requires=[
          'decorating',
          'appdirs',
          'requests'
      ],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Utilities'
      ],
      keywords='social blog cli',
      extras_require={
        "Requires-Dist": ["pypandoc"]
      },
      entry_points = {
        'console_scripts': ['kobato=kobato.command_line:main'],
      },
      zip_safe=False)
