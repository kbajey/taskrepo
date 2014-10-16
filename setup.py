from setuptools import setup

requires = [
    'pyramid==1.3',
    'requests==1.1.0',
    'boto',
    'pep8',
    'pylint==1.1.0',
    'elasticsearch>=1.0.0,<2.0.0'
]

setup(name='searchit',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = searchit:main
      """,
)
