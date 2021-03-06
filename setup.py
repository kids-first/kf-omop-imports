import os
from setuptools import setup, find_packages

# root_dir = os.path.dirname(os.path.abspath(__file__))
# req_file = os.path.join(root_dir, 'requirements.txt')
# with open(req_file) as f:
#     requirements = f.read().splitlines()

setup(
    name='kf-omop-imports',
    version='0.1',
    description='Kids First OMOP Imports',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'omop=cli:cli',
        ],
    },
    include_package_data=True
)
