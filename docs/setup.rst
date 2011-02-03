Setup
=====

If you haven't already, start by downloading Overseer. The easiest way is with *pip*::

	pip install overseer --upgrade

Or with *setuptools*::

	easy_install -U overseer

Once installed, you're going to need to configure a basic Django project. You can either use Overseer within your existing project, or
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

You may now continue to :doc:`config` for configuration options.