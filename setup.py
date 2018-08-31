from setuptools import setup, find_packages
version='0.1.4'
#with open('D:/Clouds/Dropbox/ezHDF/README.md') as file:
#    long_description = file.read()

setup(
    name = 'ezHDF',
    version = version,
    packages = ['ezHDF'],
    description = 'A convenient toolbox to store and read huge amount of data using pandas and HDF5',
    scripts = [],
    license='MIT',
    author = 'pipidog',
    author_email = 'pipidog@gmail.com',
    url = 'https://github.com/pipidog/ezHDF',
    download_url = 'https://github.com/pipidog/ezHDF/archive/v.'+version+'.tar.gz',
    keywords = ['HDF5','h5py','pandas','PyTables'],
    classifiers = ['Topic :: Utilities'],
    install_requires=['pandas','numpy','h5py']
)