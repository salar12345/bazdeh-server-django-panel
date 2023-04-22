from setuptools import setup, find_packages

__version__ = "1.0.1"

setup(
    name="bzsdp",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "Django",
        "django_extensions",
        "djangorestframework",
    ],
    entry_points={
        "console_scripts": [
            "bzsdp = bzsdp.manage:cli"
        ]
    },
)
