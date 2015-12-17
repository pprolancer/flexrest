from setuptools import setup

__version__ = '0.1.2'

setup(
    name='flexrest',
    packages=['flexrest'],
    version=__version__,
    author='pprolancer',
    author_email='pprolancer@gmail.com',
    url='https://github.com/pprolancer/flexrest',
    download_url='https://github.com/pprolancer/flexrest/tarball/%s' % __version__,
    keywords=['api', 'rest', 'restful'],
    description='Flexible Flask Rest Api',
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
    classifiers=[],
)
