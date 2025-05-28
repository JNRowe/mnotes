Personal bleet broadcaster
==========================

.. warning::

    This repo is an organic growth of hacks, although part of me *really* loves
    that.

.. epigraph::

    ``@JNRowe@eads_cs`` Time to posse that, or you'll [be] stuffed when you leave

    -- Nathan McGregor

The code in this repo is my MVP for POSSE’ing my own bleets.  It isn’t pretty,
it isn’t generic, and it isn’t likely to improve.

I add features *only* when I post a note that requires it, if you mingle the
``master`` and ``data`` branches you’ll see the development in action.  Whether
this is a good idea is left as a topic for the reader and beer.

If you like it, hate it, or have questions feel free to drop me a mail_ or open
an issue_.

Usage
-----

This is a *very* personal thing, that I’ve broken up a little to make public.
It *won’t* for you work without fettling.  If you’re me, or you want to know
what it feels like, try the following:

.. code-block:: console

   $ git clone https://github.com/JNRowe/mnotes µnotes
   $ cd !$
   $ # Try out my data repo…
   $ git clone --single-branch -b data https://github.com/JNRowe/mnotes data
   $ ./µnotes.py > output.html
   $ xdg-open !$

Other than that you’re on your own!

.. note::

   This project should be µnotes, but GitHub won’t accept µ in the repo name.

.. _mail: jnrowe@gmail.com
.. _issue: https://github.com/JNRowe/mnotes/issues
