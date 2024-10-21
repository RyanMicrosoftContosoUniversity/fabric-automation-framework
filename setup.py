from setuptools import setup, find_packages

# Open the README file.
with open(file="README.md", mode="r") as fh:
    long_description = fh.read()

setup(
    name='fabric-automation-framework',
    version='0.1.0',
    install_requires=[
        'msal',
        'azure-identity',
        'azure-keyvault-secrets',
        'requests'
    ],
    packages=find_packages(
        include=['src']
    ),
    entry_points={
        'console_scripts': [
            # Define command-line scripts here, e.g.,
            # 'metadata-scan=scripts.metadata_scan:main',
        ],
    },
    include_package_data=True,
    description='A framework for fabric automation',
    author='RH',
    author_email='RH@gmail.com',
    url='https://github.com/yourusername/fabric-automation-framework',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)