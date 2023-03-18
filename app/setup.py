from setuptools import find_packages, setup

setup(
    name='technical_challenge_ml',
    version='0.0.1',
    packages=find_packages(),
    include_packages_data=True,
    install_requires=[
        'flask',
        'requests'
    ]
)