#!/usr/bin/env python3
"""

    Element setup
    ~~~~~~~~~~~~~

"""
from pathlib import Path
from setuptools import setup, find_packages  # type: ignore


def read_readme() -> str:
    readme_file_path = Path(__file__).resolve().with_name("README.md")
    return readme_file_path.read_text("utf-8")


setup(
    name="biometrics_client",
    version="0.1.0",
    author_email="sre@crowdemotion.com",
    description=read_readme(),
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests==2.22.0", "requests-toolbelt==0.9.1"],
    extras_require={"test": ["pytest", "coverage"]},
    author="Element Human",
)
