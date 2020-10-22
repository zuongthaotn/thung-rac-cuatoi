import os
import sys

if sys.version_info < (3, 4):
    sys.exit('ERROR: Quant trading by python requires Python 3.4+')


if __name__ == '__main__':
    from setuptools import setup, find_packages

    setup(
        name='Zuongthao Quant Trading',
        description="Zuongthao quant trading strategies in Python",
        license='AGPL-3.0',
        url='https://github.com/zuongthaotn/quant-trading-by-py',
        long_description=open(os.path.join(os.path.dirname(__file__), 'README.md'),
                              encoding='utf-8').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        include_package_data=True,
        setup_requires=[
            'setuptools_git',
            'setuptools_scm',
        ],
        python_requires='>=3.4',
        author='Zuongthao'
    )
