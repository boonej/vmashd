```


                            _         _
                           | |       | |
 __   ___ __ ___   __ _ ___| |__   __| |
 \ \ / / '_ ` _ \ / _` / __| '_ \ / _` |
  \ V /| | | | | | (_| \__ \ | | | (_| |
   \_/ |_| |_| |_|\__,_|___/_| |_|\__,_|





```

# vmashd

VMASHD is a tool to create generate video/audio from a set of audio, video, and
text inputs. It is build on top of the
[moviepy](https://github.com/Zulko/moviepy) library and provides a simple
command line interface with little configuration required.

## Quickstart

### Installation

Install the command with:

```
pip install vmashd

```

### Configure Directories

VMASHD requires a configuration file to be present. To set up a default file,
run:

```
vmashd config

```

Make note of the file path and make any changes that you require. No Directories
are created at this point.

### Create Directories

Once your configuration file is configured to your liking, run:

```
vmashd makedirs

```

All required directory structures will be created.

### Add files

Add at least one audio file and as many video files as possible to their
respective directories.

### Mash

Once all files are present, execute:

```
vmashd mashup --filename /path/to/file.mp4

```

Read the docs for extra options.

## Example

This example generates a collage of the provided inputs without applying any
effects to the subclips. The path provided for filepath (with the exception of
the actual file).

```
vmashd mashup --no-randfx --filename /path/to/file.mp4

```
