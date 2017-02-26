try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools

    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - pre-alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: Apache License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development']
setup(name='HAWK',
      version='1.0.0',
      author='Supratik Banerjee',
      author_email='supratikbanerjee13@gmail.com',
      description='An SDK built to facilitate application development for UAVs.',
      license='Apache License 2.0',
      classifiers=classifiers,
      url='https://github.com/supratikbanerjee/HAWK',
      packages=find_packages())
