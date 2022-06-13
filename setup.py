from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    scripts=[],
    include_package_data = True,
    install_requires=[
        'kachery-cloud>=0.1.15',
        'figurl',
        'pyvips'
    ]
)
