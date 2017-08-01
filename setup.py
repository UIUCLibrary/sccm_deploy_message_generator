from setuptools import setup
import os

metadata = {}
metadata_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'deploy_message', '__version__.py')

with open(metadata_file, 'r', encoding='utf-8') as f:
    exec(f.read(), metadata)
with open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name=metadata["__title__"],
    version=metadata["__version__"],
    packages=['deploy_message'],
    url=metadata["__url__"],
    license=metadata["license_"],
    install_requires=["PyYAML", "Jinja2"],
    author=metadata["__author__"],
    author_email=metadata["__author_email__"],
    maintainer=metadata["maintainer"],
    maintainer_email=metadata["maintainer_email"],
    description=metadata["__description__"],
    download_url=metadata["download_url"],
    entry_points={
        "console_scripts": [
            "deploymessage =deploy_message.__main__:main"
        ]
    },
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

)
