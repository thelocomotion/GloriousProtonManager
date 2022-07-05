from setuptools import setup, find_packages

setup(
    name='GloriousProtonManager',
    version='0.1',
    description='Manage GE-Proton',
    license='GNU General Public License v3 (GPLv3)',
    author="Loco Motion",
    author_email='thelocomotionnn@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/thelocomotion/GloriousProtonManager',
    keywords='proton proton-ge wine linux valve',
    install_requires=[
          'PySimpleGUI',
      ],
)
