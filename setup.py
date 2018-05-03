from distutils.core import setup

setup(
    name='iofog-container-sdk',
    version='1.0.5',
    packages=['iofog_container_sdk'],
    url='http://iofog.org',
    license='EPL-2.0',
    author='Eclipse ioFog',
    author_email='edgemaster@iofog.org',
    description='Native python SDK for Eclipse ioFog development.',
    requires=['ws4py'],
    keywords='iofog, IoT, Eclipse, fog, edgeworx',
)
