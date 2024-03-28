"""
setup.py setup script

@author: roland@adaminformatika.hu
"""

import sys
import os

from setuptools import setup, find_packages


package_app_path = os.path.abspath('./sa')

if package_app_path not in sys.path:
    sys.path.insert(0, package_app_path)

if package_edc_client_path not in sys.path:
    sys.path.insert(0, package_edc_client_path)

with open('requirements.txt', encoding="utf-8") as f:
    required = f.read().splitlines()
    print(required)

setup(
    name='sa_logic',
    version='0.0.1',
    packages=[
        'sa',
    ],
    package_dir={
        'sa': 'sa',
    },
    url='',
    license='',
    author=[{'email': 'roland@adaminformatika.hu'}],
    description='sentyment analysis logic app',
    install_requires=required,
)
