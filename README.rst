::


                              _         _
                             | |       | |
   __   ___ __ ___   __ _ ___| |__   __| |
   \ \ / / '_ ` _ \ / _` / __| '_ \ / _` |
    \ V /| | | | | | (_| \__ \ | | | (_| |
     \_/ |_| |_| |_|\__,_|___/_| |_|\__,_|





vmashd
######

**vmashd** is a command-line tool built on top of the
`moviepy <https://zulko.github.io/moviepy/>`_ library. It takes subclips from a
directory of movie files and randomly forms a video set to one or more audio
files.

.. note::

  This project is under active development.

Usage
=====

.. _installation:

Installation
------------

Install vmashd with pip:

.. code-block:: console

  pip install vmashd

.. _configuration:

Configuring vmashd for your environment
---------------------------------------
Some configuration is required prior to generating video mixes. Before use run:

.. code-block:: console

  vmashd config

This will generate a default configuration file and print the contents to the
console. The directories will not be created at this point. If you would like
to change any of the file paths, edit the config file in your text editor of
choice.

Create any missing directory structure by executing:

.. code-block:: console

  vmashd makedirs

If you would like to add titles (at random of course) throughout the video,
provide a path a text file in the config file. The text file should have each
caption on a separate line. Ex:

.. code-block:: console

  eat beef
  it is delicious
  beef makes you better
  mooooooo

Font, position, and color can be modified in the configuration file. To see
a list of fonts available (it will be long) execute:

.. code-block:: console

  vmashd listfonts


.. _mashup:

Creating a video mashup
-----------------------

After the configuration is commplete, the rest is pretty simple. You will need:

1. one or more audio files stored in the audio directory; make sure they will
not be filtered out by the audio filter string.
2. one or more video files (more is better) stored in the video directory;
they should at least 5 seconds long.

If the above conditions are met, execute:

.. code-block:: console

  vmashd mash --filename ./filepath.mp4


Optionally, you can enable video effects to be randomly inserted into the
video:

.. code-block:: console

  vmashd mash --randfx --filename ./filepath.mp4

A soft blur can be applied to the length of the video:

.. code-block:: console

  vmash mash -f filepath.mp4 --blur --randfx
