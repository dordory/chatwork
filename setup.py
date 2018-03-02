from setuptools import setup, find_packages

setup(name='ChatworkWrapper',
      version='0.1',
      url="",
      license='MIT',
      author='SeongUk Yun',
      author_email='dordory@gmail.com',
      description='Chatwork API Wrapper',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=[''],
      test_suite='nose.collector')
