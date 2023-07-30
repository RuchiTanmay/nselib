import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nselib',
    packages=setuptools.find_packages(),
    version='0.7',
    include_package_data=True,
    description='library to get NSE India data',
    long_description=long_description,
    long_description_content_type="text/markdown", author='RuchiTanmay',
    author_email='ruchitanmay@gmail.com',
    url='https://github.com/RuchiTanmay/nselib',
    install_requires=['requests', 'pandas', 'scipy'],
    keywords=['nseindia', 'nse', 'python', 'sdk', 'trading', 'stock markets'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
