Pytriloquist
============

Pytriloquist is a `Python`_-based Bluetooth remote control app for
`S60 5th Edition`_ devices. I developed this app in two weekends while
exploring my brand new smartphone, the good `Nokia 5800 Xpress Music`_.


:Author:  Daniel Fernandes Martins <daniel@destaquenet.com>
:Company: `Destaquenet Technology Solutions`_

    
Features
--------

* Multi-lingual interface (English and Brazilian Portuguese);
* Configurable applications and commands;
* Rich touchpad support that emulates a two-button mouse with vertical and
  horizontal scrollbars;


.. warning::
  This app is just a prototype; it's not intended to be used "in production".
  If you do so, do at your own risk.


Requirements
------------

Client app
``````````

* S60 5th Edition smartphone with touch support;
* `Python for S60`_ 1.9.7+ with Python Script Shell;

Server app
``````````

* Linux operating system with Bluetooth card;
* `Python`_ 2.5+;
* Python Bluetooth stack (like `PyBluez`_);
* `xautomation`_ (used to reproduce the mouse gestures on the X11 server);


Installation
------------

Since this app is just a prototype, I would probably never bother to create a
native SIS package for it. This makes the installation a non-trivial task:

1. Create the directory ``E:/data/pytriloquist`` on your device;
2. Copy the ``locale`` directory there;
3. Copy the files ``src/pytriloquist_cli.py`` and ``src/pytriloquist`` to
   ``E:/data/python`` [1]_;
4. Open the Python Script Shell and choose ``pytriloquist_cli.py`` to start the
   app.


Usage
-----

Server app
``````````

Run the following command to start up the server::

    $ python src/pytriloquist_srv.py [-c CHANNEL]


Client app
``````````

Run the app using the Python Script shell and open the Settings dialog to
configure it.

`Python for S60`_ has some serious issues with ``btsocket.bt_discover()``,
which is the function used to perform Bluetooth device/service lookup. Thus,
you are required to configure the server address manually using the Settings
dialog. Run ``hcitool dev`` on the server to find out the address of your
bluetooth card.

Once configured, you can use the input touchpad and add commands for your
favourite applications.


FAQ
---

Is it just for Linux?
`````````````````````

Yes, although you can easily adapt the app to make it work on other operating
systems as well. But that's up to you.


What do you think of Python for S60?
````````````````````````````````````

The Python port for the S60 platform is a work in progress, so expect lots of
bugs and shortcomings. If you pretend to create professional apps for S60, do
it in C++.


.. [1] If your device keeps the Python sample apps in a differect directory,
   please use the correct directory and change ``src/pytriloquist_cli.py`` to
   point to that directory.


.. _Python: http://www.python.org
.. _PyBluez: http://code.google.com/p/pybluez/
.. _Python for S60: http://garage.maemo.org/projects/pys60
.. _S60 5th Edition: http://en.wikipedia.org/wiki/S60_%28software_platform%29
.. _Nokia 5800 Xpress Music: http://www.nokia.co.uk/find-products/all-phones/nokia-5800
.. _xautomation: http://hoopajoo.net/projects/xautomation.html

.. _Destaquenet Technology Solutions: http://www.destaquenet.com/
