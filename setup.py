from setuptools import setup

setup(
    name='certificates',
    version='0.1.0',
    packages=['certificates'],
    install_requires=[
        'click',
        'lxml',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'certificates=certificates.__main__:main',
        ]
    }
)
