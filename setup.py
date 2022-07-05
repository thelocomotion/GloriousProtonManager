from setuptools import setup, find_packages

setup(
    name='GloriousProtonManager',
    version='0.22',
    python_requires='>=3.10',
    description='Manage GE-Proton with a simple UI',
    license='GNU General Public License v3 (GPLv3)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="CDT",
    author_email='thelocomotionnn@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/thelocomotion/GloriousProtonManager',
    keywords='proton proton-ge wine linux valve',
    install_requires=[
        'PySimpleGUI'
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
