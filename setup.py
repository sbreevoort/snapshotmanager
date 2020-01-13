from setuptools import setup

setup(
    name='Snapshotmanager',
    version='0.1',
    author='.S.B.',
    description='Snapshotmanager is a tool to manage snapshots of AWS EC2 instances',
    packages=['src'],
    url='www.url.com',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        snapshotmanager=src.snapshotmanager:cli
    '''
)
