from setuptools import setup, find_packages

setup(
    name='Annuaire des anciens',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['werkzeug>=0.9',
                      'jinja2>=2.7',
                      'Flask>=0.10',
                      'Flask-Login>=0.2',
                      'sqlalchemy',
                      'psycopg2>=2.4',
                      'WTForms',
                      'requests',
                      'lxml'
                      ]
)