from setuptools import setup

import kobato

with open('requirements.txt', 'r', encoding='UTF-8') as f:
    requirements = list(map(str.strip, f.readlines()))

setup(name=kobato.__name__,
      version=kobato.__version__,
      description='A command line interface to your point.im blog',
      url=kobato.__url__,
      download_url='{url}/tarball/{version}'.format(url=kobato.__url__, version=kobato.__version__),
      author=kobato.__author__,
      author_email=kobato.__email__,
      license='GNU/GPLv3+',
      packages=['kobato', 'kobato.commands', 'kobato.editor'],
      install_requires=requirements,
      # https://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Utilities'
      ],
      keywords='social blog cli',
      entry_points={
        'console_scripts': ['kobato=kobato.cli:main'],
      },
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      package_data={
          'kobato': ['templates/*.jinja']
      }
      )
