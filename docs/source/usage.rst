Usage
=====

.. _installation:

Installation
------------

Install vmashd with pip:

.. code-block:: console

  pip install vmashd

.. _configuration:

Creating a default configuration file
---------------------------------------
Some configuration is required prior to generating video mixes. Execute the
**config** command to generate a default configuration file.

.. code-block:: console

  vmashd config

This will generate a default configuration file and print the contents to the
console. The directories will not be created at this point. If you would like
to change any of the file paths, edit the config file in your text editor of
choice. The folders do not need to exist.

.. _generatefolders:

Generate directory structure
-----------------------------

Create missing directory structures defined in the configuration file by
executing:

.. code-block:: console

  vmashd makedirs

The tool should only attempt to create directories that do not exist. Nested
directories are permitted.

.. _titles:

Random titles
--------------

If you would like to add titles (at random of course) throughout the video,
provide the path to a text file in the config file. The text file should have each
caption on a separate line. Ex:

.. code-block:: console

  eat beef
  it is delicious
  beef makes you better
  mooooooo

.. _execution:

Creating a video mashup
-----------------------

After the configuration is complete, the rest is pretty simple. You will need:

1. one or more audio files stored in the audio directory; make sure they will
not be filtered out by the audio filter string.

2. one or more video files (more is better) stored in the video directory;
they should at least 5 seconds long.

If the above conditions are met, execute:

.. code-block:: console

  vmashd mashup --filename ./filepath.mp4


Optionally, you can enable video effects to be randomly inserted into the
video:

.. code-block:: console

  vmashd mashup --randfx --filename ./filepath.mp4

.. _configtricks:

Config File Tricks
------------------

Filtering videos
`````````````````

Adjust the video filter to select the file type that you provide. By default,
only files with an extension that matches ``*.m*``. If you alter it to select
all files, ensure that your captions file is located elsewhere.

Weighting videos
`````````````````

Videos are automatically weighted based on length. This prevents repeated clips
from a shorter video. The config file allows you to set a filter to select
videos that should be excluded from weighting. This means that any file matching
the filter would be weighted as a shorter video despite its length.
