from matplotlib.pyplot import install_repl_displayhook
from setuptools import setup

setup(name='tom_stock_common',
        version='0.1',
        description='For my daily use and trading bot',
        url='https://github.com/ymlai87416/stock_tools',
        author='ymlai87416',
        author_email='ymlai87416@gmail.com',
        license='copyright',
        packages=['tom_stock_common', 'tom_stock_common.data', 'tom_stock_common.notification'],
        install_requires=[
            'PyYAML', 'pandas', 'pandas-datareader',
            'alpaca-trade-api',
            'google-api-core',
            'google-api-python-client',
            'google-auth',
            'google-auth-httplib2',
            'google-auth-oauthlib',
            'googleapis-common-protos',
            'yfinance',
        ],
        zip_safe=False
)