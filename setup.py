from setuptools import setup, find_namespace_packages

setup(
    name='Apartment_Alert',
    version='1.0',
    description='E-Mail notifications whenever a new suitable apartment is offered online.',
    author='Lukas Humpe',
    author_email='l.humpe@hotmail.de',
    packages=find_namespace_packages(include=['*']),
    install_requires=['schedule', 'requests', 'beautifulsoup4', 'click','lxml'],
    entry_points={'console_scripts': ['ApartmentAlert=ApartmentAlert.cli.cli:cli']}
)
