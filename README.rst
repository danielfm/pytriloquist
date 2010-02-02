Pytriloquist
============

Pytriloquist is a `Python`_-based Bluetooth remote control app for
`S60 5th Edition`_ devices. I developed this app in two weekends while
exploring my brand new smartphone, a `Nokia 5800 Xpress Music`_.


:Author:  Daniel Fernandes Martins <daniel@destaquenet.com>
:Company: `Destaquenet Technology Solutions`_

    
Features
--------

* Multi-lingual interface (English and Brazilian Portuguese);
* Configurable applications and commands;
* Full touchpad support.


.. warning::
  This app is just a prototype; it's not intended to be used "in production".
  If you do so, do at your own risk.


Server App
----------

Requirements
````````````

* Linux operating system with Bluetooth card;
* `Python`_ 2.5+;
* Python Bluetooth stack (like `PyBluez`_);
* `xautomation`_ (used to reproduce the mouse gestures on the X11 server).


Usage
`````

Run the following command to start up the server::

    $ python src/server/pytriloquist.py [-c CHANNEL]


Client App
----------

Requirements
````````````

* `S60 5th Edition`_ device with touch support;
* `Python for S60`_ 1.9.7+;


Build and Install
`````````````````

To be able to package the client app to a .sis file, you need to download and
extract `Python for S60`_ to your computer.

Then, open ``Makeconf`` and change the ``PYS60_DIR`` variable to make it point
to that directory.

Finally, run ``make`` to build two packages:

1. A .sis package (unsigned);
2. A .sisx package (signed with the built-in certificates).

Just upload the appropriate package to your device to install it.


Usage
`````

On your device, open the Applications menu and launch Pytriloquist from there.

`Python for S60`_ has some serious issues with ``btsocket.bt_discover()``,
which is the function used to perform Bluetooth device/service lookup. Thus,
you are required to configure the server address manually using the Settings
dialog. Run ``hcitool dev`` on the server to find out the address of your
bluetooth card.

Once configured, you can use the input touchpad and add commands to be executed
on the server.


Touchpad Gestures
'''''''''''''''''

The three mouse buttons are located on the bottom-left corner of the screen,
and the light gray rectangles are the scrollbars.

It works pretty much like a laptop's touchpad. The only exception is the drag
and drop gesture; touch the mouse button, move the finger/stylus outside the
button area and release to start dragging. Touch the button again to stop.


FAQ
---

Is it just for Linux?
`````````````````````

Yes, although you can easily modify the server script to make it work with
other operating systems as well. But that's up to you.


What do you think of Python for S60?
````````````````````````````````````

The Python port for the S60 platform is a work in progress, so expect lots of
bugs and shortcomings. If you pretend to create professional apps for S60, do
it in C++.


.. _Python: http://www.python.org
.. _PyBluez: http://code.google.com/p/pybluez/
.. _Python for S60: http://garage.maemo.org/projects/pys60
.. _S60 5th Edition: http://en.wikipedia.org/wiki/S60_%28software_platform%29
.. _Nokia 5800 Xpress Music: http://www.nokia.co.uk/find-products/all-phones/nokia-5800
.. _xautomation: http://hoopajoo.net/projects/xautomation.html

.. _Destaquenet Technology Solutions: http://www.destaquenet.com/
