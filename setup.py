#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()

setup(
    name='Overseer',
    version='0.2.2',
    author='DISQUS',
    author_email='opensource@disqus.com',
    url='http://github.com/disqus/overseer',
    description = 'A status board built with Django',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Django>=1.2.4',
        'South',
        'django-devserver',
        'oauth2>=1.5.169',
        'uuid',
    ],
    license='Apache License 2.0',
    test_suite = 'overseer.tests',
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)