Overseer is a simple status board app written in Django.

Screenshot
==========

.. image:: http://f.cl.ly/items/0p1r3S1V3D0h1K183a3D/Screen%20shot%202011-01-20%20at%205.47.59%20PM.png

Install
=======

Simply use pip, or easy_install::

  pip install overseer

Setup
=====

You're first going to need to configure a basic Django project. You can either use Overseer within your existing project, or
base it on the provided shell in ``example_project``.

Existing Project
----------------

To use it within an existing project, adjust the following in ``settings.py``::

  INSTALLED_APPS = (
      ...
      'overseer',
  )

You'll also need to include the appropriate ``urls.py``::

  urlpatterns = patterns('',
      (r'^status', include('overseer.urls', namespace='overseer')),
  )

New Project
-----------

Simple copy the ``example_project`` directory included with the package, and adjust ``settings.py` as needed.

Configuration
=============

Several configuration variables are available within Overseer. All of these are handled with a single dictionary configuration object::

  OVERSEER_CONFIG = {
      # the title for your page
      'TITLE': 'DISQUS Service Status',
      
      # the heading text for your page
      'NAME': 'status.disqus.com',

      # the prefix for overseer's media -- by default this is handled using Django's static media server (pre-1.3)
      'MEDIA_PREFIX': '/status/media/',
  }


Administration
==============

As of the current version, the only way to administer the application is via the ``django.contrib.admin`` integration.