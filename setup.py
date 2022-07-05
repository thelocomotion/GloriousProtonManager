from setuptools import setup, find_packages

setup(
    name='GloriousProtonManager',
    version='0.0.11',
    license='GNU General Public License v3 (GPLv3)',
    author="Loco Motion",
    author_email='thelocomotionnn@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/thelocomotion/GloriousProtonManager',
    keywords='example project',
    install_requires=[
          'PySimpleGUI',
          'requests',
          'urllib3',
      ],
)
