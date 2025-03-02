#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

setup(name='pipelinewise-tap-snowflake',
      version='2.3.2',
      description='Singer.io tap for extracting data from Snowflake - PipelineWise compatible',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="TransferWise",
      url='https://github.com/transferwise/pipelinewise-tap-snowflake',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=['tap_snowflake'],
      install_requires=requirements,
      entry_points='''
          [console_scripts]
          tap-snowflake=tap_snowflake:main
      ''',
      packages=['tap_snowflake', 'tap_snowflake.sync_strategies'],
)
