from setuptools import setup, find_packages
from os.path import abspath, dirname, join

CWD = abspath(dirname(__file__))


setup(
    name="robotframework-seleniumproxy",
    author="Dillan Teagle",
    author_email="dillan@teaglebuilt.com",
    url="https://github.com/teaglebuilt/robotframework-seleniumproxy",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Extends Selenium to give you the ability to inspect requests made by the browser.",
    install_requires=['selenium>=3.4.0'],
    license="MIT",
    packages=find_packages("src"),
    package_dir={'': 'src'},
    version='0.0.1'
)
