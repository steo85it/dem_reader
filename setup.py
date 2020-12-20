import setuptools

setuptools.setup(
    name='dem_reader',
    version='0.1.0',
    author='Stefano Bertone',
    # author_email='you@yourdomain.com',
    description='Simple script to extract elevation data at list of coordinates',
    platforms='Posix; MacOS X; Windows',
    packages=setuptools.find_packages(where='./dem_reader'),
    package_dir={
        '': 'dem_reader'
    },
    include_package_data=True,
    install_requires=(
        'numpy','pandas','time','xarray','pyproj','pygmt'
    ),
    # setup_requires=(
    #     'pytest-runner',
    # ),
    # tests_require=(
    #     'pytest-cov',
    # ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
