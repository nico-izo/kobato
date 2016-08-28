from setuptools import setup

setup(name='kobato',
      version='0.1',
      description='A command line interface to your point.im blog',
      url='https://github.com/nico-izo/kobato',
      download_url = 'https://github.com/nico-izo/kobato/tarball/0.1',
      author='Nicolay Izoderov',
      author_email='nico-izo@ya.ru',
      license='GNU/GPLv3',
      packages=['kobato', 'kobato.commands'],
      install_requires=[
          'decorating',
          'appdirs',
          'requests',
          'pyyaml'
      ],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Utilities'
      ],
      keywords='social blog cli',
      entry_points = {
        'console_scripts': ['kobato=kobato.command_line:main'],
      },
      zip_safe=False)
