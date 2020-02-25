import versioneer
from setuptools import setup, find_packages
from os.path import abspath, dirname, join


CWD = abspath(dirname(__file__))

with open(join(CWD, "requirements.txt"), encoding="utf-8") as f:
    REQUIREMENTS = f.read().splitlines()

with open(join(CWD, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

CLASSIFIERS = """
Development Status :: 4 - Beta
Intended Audience :: Developers
Topic :: Software Development :: Testing
License :: OSI Approved :: MIT License
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
""".strip().splitlines()

setup(
    name="robotframework-seleniumproxy",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Capture requests/responses generated with Seleniums Webdriver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dillan Teagle",
    author_email="dillan@teaglebuilt.com",
    url="https://github.com/teaglebuilt/robotframework-seleniumproxy",
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    keywords="selenium webdriver proxy robotframework seleniumlibrary network activity request response",
    license="MIT",
    packages=find_packages("src"),
    package_dir={'': 'src'}
)
