"""
REST client for Teradata's DMC API
"""
from setuptools import setup

def readme():
    """Use README file as long_description"""
    with open('README.md') as readme_f:
        return readme_f.read()

setup(
    name='pydmc',
    version='0.1.1',
    description='REST client for Teradata\'s DMC API',
    long_description=readme(),
    url='https://github.com/TeradataInteractiveAmericas/pydmc',
    author='Nick Silva',
    author_email='nick.silva@teradata.com',
    license='MIT',
    packages=['pydmc'],
    install_requires=[
        'requests',
    ],
    zip_safe=False)
