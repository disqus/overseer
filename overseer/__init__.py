"""
Overseer
~~~~~~~~
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('Overseer').version
except Exception, e:
    VERSION = 'unknown'
