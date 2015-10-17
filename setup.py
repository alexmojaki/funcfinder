from setuptools import setup

setup(name='funcfinder',
      version='0.1',
      description='A tool for automatically solving problems of the form "I need a python function that does X."',
      url='https://github.com/alexmojaki/funcfinder',
      author='Alex Hall',
      author_email='alex.mojaki@gmail.com',
      license='MIT',
      packages=['funcfinder'],
      zip_safe=False,
      entry_points={
          'console_scripts': ['funcfinder=funcfinder.__main__:main'],
      },
      requires=['wrapt'])
