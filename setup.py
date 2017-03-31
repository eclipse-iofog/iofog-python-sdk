from distutils.core import setup

setup(
    name='iofog-container-sdk',
    version='2.0',
    packages=['client'],
    url='http://iotracks.com/',
    license='',
    author='iotracks',
    author_email='kilton@iotracks.com',
    description='Native python SDK for ioTracks development.',
    requires=['ws4py'],
    keywords='iotracks, IoT',
)
