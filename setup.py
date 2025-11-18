from setuptools import setup, find_packages

# Read the version from __version__.py
with open("espn_scores/__version__.py", "r") as f:
    version_line = f.read().strip()
    version = version_line.split("=")[1].strip().strip('"')

# Read the README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="espn-scores",
    version=version,
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Python package for interacting with the ESPN Scoreboard API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/espn-scores",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
    },
    keywords="espn sports scores nfl nba mlb api",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/espn-scores/issues",
        "Source": "https://github.com/yourusername/espn-scores",
    },
)
