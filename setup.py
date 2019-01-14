import setuptools
from setuptools import find_packages

import gwap_framework


def long_description():
    with open('README.md', encoding='utf8') as f:
        return f.read()


setuptools.setup(
    name='gwap-framework',
    version=gwap_framework.__version__,

    url='https://bitbucket.org/serasaecs/ecs-lib-boleto-python',
    description='Biblioteca padrão de framework para aplicações em Python no GWAP.',
    long_description=long_description(),
    long_description_content_type="text/markdown",

    author='Guilherme Dalmarco',
    author_email='dalmarco.br@gmail.com',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],

    include_package_data=True,
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'redis==2.10.6',
        'flask==1.0.2',
        'flask-restful==0.3.6',
        'redis==2.10.6',
        'python-decouple==3.1',
        'schematics==2.1.0',
        'aiohttp==3.4.4',
        'pyjwt==1.7.0',
        'sqlalchemy==1.2.12',
    ],
    extras_require={},
)
