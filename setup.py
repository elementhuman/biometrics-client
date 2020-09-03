#!/usr/bin/env python3
"""

    Element setup
    ~~~~~~~~~~~~~

"""
import sys
import shlex
import subprocess
from pathlib import Path
from setuptools import setup, find_packages  # type: ignore
from setuptools.command.develop import develop  # type: ignore
from typing import List


def read_readme() -> str:
    readme_file_path = Path(__file__).resolve().with_name("README.md")
    return readme_file_path.read_text("utf-8")


def parse_reqs(requirements_file: str) -> List[str]:
    """Get requirements as a list of strings from the file."""
    with open(requirements_file) as f:
        return [i.rstrip() for i in f.readlines()]


class CustomDevelop(develop):
    """Develop command that actually prepares the development environment."""

    def run(self) -> None:
        """Setup the local dev environment fully."""
        super().run()

        for command in [
            "pip --version",
            "pip install -r dev_requirements.txt",
            "pip install -r requirements.txt",
        ]:
            print("\nCustom develop - executing:", command, file=sys.stderr)
            subprocess.check_call(shlex.split(command))


setup(
    name="eh-biometrics-client",
    version="0.0.1",
    url="https://github.com/elementhuman/biometrics-client",
    author="Element Human",
    description=read_readme(),
    packages=find_packages(exclude=["tests"]),
    install_requires=parse_reqs("requirements.txt"),
    extras_require={"test": ["pytest", "coverage"]},
    cmdclass={"develop": CustomDevelop},
)
