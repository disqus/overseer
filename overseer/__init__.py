"""
Overseer
~~~~~~~~
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('overseer').version
except Exception, e:
    VERSION = 'unknown'
