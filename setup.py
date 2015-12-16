from setuptools import setup, find_packages

__version__ = 'dev'

setup(
    name='flexrest',
    version=__version__,
    author='pprolancer@gmail.com',
    description='Flexible Flask Rest Api',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
    ],
    entry_points={
    },
    dependency_links=[
    ],
    install_requires=[
        'flask',
        'flask-principal',
        'formencode',
        'sqlalchemy',
    ],
    classifiers=['Development Status :: 1 - Production/Beta',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Topic :: Internet :: WWW/HTTP',
                 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                 'Topic :: Software Development :: Libraries :: Application Frameworks',
                 'Topic :: Software Development :: Libraries :: Python Modules', ],
)
