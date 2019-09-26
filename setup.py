import os

from setuptools import setup, find_packages


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


setup(
    name='dataproc',
    version='0.0.1',
    description='Data Processing and Transformation',
    author='Alef Bruno Delpino',
    author_email='alefdelpino@gmail.com',
    url='https://github.com/Delpinos/dataproc',
    license='GPL License',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    keywords='dataproc proc data etl tramsform process pipeline executor',
    packages=find_packages(),
    install_requires=parse_requirements('/'.join([os.path.abspath(os.path.dirname(__file__)), 'requirements.txt']))
)
