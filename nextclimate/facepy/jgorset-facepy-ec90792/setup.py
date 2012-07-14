from setuptools import setup

readme = open('README.rst').read()
history = open('HISTORY.rst').read()

execfile('facepy/version.py')

setup(
    name = 'facepy',
    version = __version__,
    description = 'Facepy makes it absurdly easy to interact with Facebook APIs',
    long_description = readme + '\n\n' + history,
    author = 'Johannes Gorset',
    author_email = 'jgorset@gmail.com',
    url = 'http://github.com/jgorset/facepy',
    packages = ['facepy'],
    install_requires = ['requests >=0.8, < 0.11'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
