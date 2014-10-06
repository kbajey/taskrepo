from setuptools import setup

requires = [
    'pyramid==1.3',
]

setup(name='searchit',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = searchit:main
      """,
)
