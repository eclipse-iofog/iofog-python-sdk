from distutils.core import setup

setup(
    name='iofog-python-sdk',
    version='0.0.1',
    project_urls={
        'Documentation': 'https://github.com/ioFog/iofog-python-sdk/blob/master/README.md',
        'Source': 'https://github.com/ioFog/iofog-python-sdk.git',
        'Tracker': 'https://github.com/ioFog/iofog-python-sdk/issues',
        'Eclipse ioFog': 'http://iofog.org'
    },
    packages=['iofog_python_sdk'],
    url='https://github.com/ioFog/iofog-python-sdk',
    license='EPL-2.0',
    author='Eclipse ioFog',
    author_email='edgemaster@iofog.org',
    description='Native python SDK for Eclipse ioFog development.',
    requires=['ws4py'],
    keywords='iofog IoT Eclipse fog computing edgeworx',
)
