from setuptools import find_packages, setup

setup(
    name='animedatagrablib',
    packages=find_packages(include=["animedatagrablib"]),
    version='0.1.0',
    description='Functions used to help create webscrapers',
    author='Benjamin McGregor',
    license='MaePloyKitchen',
    install_requires=[],
    setup_requires=['bs4'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)