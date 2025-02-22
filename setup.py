from setuptools import setup, find_packages

setup(
    name="temporal-features",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "click>=7.0",
    ],
    entry_points={
        'console_scripts': [
            'temporal-features=temporal_features.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for generating temporal feature derivatives",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/temporal-features",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 