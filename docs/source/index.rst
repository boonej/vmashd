.. Video Automator documentation master file, created by
   sphinx-quickstart on Sat Apr 16 21:31:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

::


                              _         _
                             | |       | |
   __   ___ __ ___   __ _ ___| |__   __| |
   \ \ / / '_ ` _ \ / _` / __| '_ \ / _` |
    \ V /| | | | | | (_| \__ \ | | | (_| |
     \_/ |_| |_| |_|\__,_|___/_| |_|\__,_|




vmashd
===========================================

**vmashd** is a command-line tool built on top of the
`moviepy <https://zulko.github.io/moviepy/>`_ library. It takes subclips from a
directory of movie files and randomly forms a video set to one or more audio
files.

.. _how:

How it works
-------------

Audio files are concatenated (no crossfade - yet) and normalized to avoid
differing volume outputs between songs. Short video clips are then (mostly)
randomly joined together from any video clips in the specified directory to
match the length of the combined audio. Video files are weighted by length to
make sure a short clip doesn't appear in a disproportionate amount.

.. _captions:

Captions
--------

Captions can be added (at random) by providing a text file. Currently no other
configuration options are provided, but they are planned.

.. note::

  Install `ImageMagick <https://imagemagick.org/index.php>`_ prior to adding
  captions to your video. Linux and MacOs should identify the libraries without
  additional configuration. Windows users should reference moviepy's
  `documentation <https://zulko.github.io/moviepy/install.html#other-optional-but-useful-dependencies>`_.

.. _fx:

Effects
-------

Random effects can be applied to random video clips. See the :doc:`usage`
section for more information.

A blur effect can be applied across the entire video using the `--blur` option.


Contents
`````````

.. toctree::

  usage

  help

  reference
