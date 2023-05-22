"""
setup.py setup script

@author: yuan.gao@zeiss.com
"""

import sys
import os

from setuptools import setup, find_packages


package_app_path = os.path.abspath('./edc_lineage')
package_edc_client_path = os.path.abspath('./edc_client')

if package_app_path not in sys.path:
    sys.path.insert(0, package_app_path)

if package_edc_client_path not in sys.path:
    sys.path.insert(0, package_edc_client_path)

with open('requirements.txt', encoding="utf-16") as f:
    required = f.read().splitlines()
    print(required)

setup(
    name='catalog_scripts',
    version='0.0.1',
    packages=[
        'edc_lineage',
        'edc_client'
    ],
    package_dir={
        'edc_lineage': 'edc_lineage',
        'edc_client': 'edc_client'
    },
    url='',
    license='',
    author=[{'email': 'yuan.gao@zeiss.com'}],
    description='scripts for datalog operations',
    install_requires=required,
)
