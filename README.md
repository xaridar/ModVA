# ModVA

ModVA, or Modular Voice Assistant, is a Python voice assistant designed for customizability and modularity. The speech recognition model can be changed in `config.yml`, and commands can be added dynamically using individual modules.

## General Configuration

In `config.yml`, several variables can be edited to change the behavior of ModVA. These are as follows:

-   ### **parser** (required)

    the `parser` variable can be edited to change to speech recognition (speech-to-text) model used for ModVA's command recognition. Currently, the supported options are:

    -   `google` - uses Google Speech Recognition API
    -   `whisper` - uses a local version on the OpenAI Whisper model for recognition
    -   `whisperapi` - uses a web API version of OpenAI's Whisper Speech Recognition model
        -   this option requires a `.env` file with a valid OPENAI_API_KEY defined in the root directory

-   ### **mods_dir** (required)

    the `mods_dir` variable specifies the directory for ModVA to use to discover [modules](#modules)

-   ### **verbose_tts**

    if `verbose_tts` is included and is true, all TTS (Text-to-Speech) messages said by ModVA will first be printed to `stdout`

-   ### **verbose_sst**

    if `verbose_sst` is included and is true, all SST (Speech-to-Text) messages interpreted by ModVA will first be printed to `stdout`

-   ### **middleware**

    `middleware` accepts an ordered list of module names, and specifies the order for [middleware](#defining-middleware) to be executed, both tts middleware and sst middleware. Any modules not listed in this variable that include middleware will still work, but the middleware will not execute.

## Modules

To define a new module, just create a new directory under the `modules` folder (or whatever directory is specified in config.yml). In this folder should be a `config.ini` file, where commands are specified; as well as at least one implementation python script. More files may be in the module for individual implementations.

`config.ini` should contain entries for each command that is a part of the module (as well as any middleware or `@init` command). This is done by having 3 required attributes, and 1 optional one, per command, with the actual commands being implemented in separate Python functions.

These attributes are:

-   ### **command** (required)

    This contains the uncapitalized string which will trigger the given command.

    -   Parameters within a command are possible, and can be specified using curly braces `{}` containing a variable name. Each argument will be accessible via Python when called.

-   ### **alt_cmds**

    `alt_cmds` is optional and contains a comma-separated list of quote-wrapped aliases for `command`. Each of the alternate commands should contain the same parameter names as `command`.

-   ### **impl_file** (required)

    This specifies the relative path to the Python source file that contains the implementation for the command. This should not contain an extension, but be formatted similarly to a module import.

-   ### **impl_fn** (required)

    This is the name of the function in `impl_file` that is to be run on command invocation.

    Each function is passed two parameters (name does not matter): `args` (of type `util.Arguments`) and `funcs` (of type `util.Functions`). `args` has members for each of the specified parameters in `command`, and `funcs` has the functions `say()`, `exit()`, and `prompt()` for interaction with ModVA.

An example of a `module` with one command, called 'say', is:

`config.ini`:

```ini
[say]
command=say {script}
alt_cmds="speak {script}"
impl_file=impl
impl_fn=say
```

`impl.py`:

```py
def say(args, funcs):
    funcs.say(args.script)
```

## Defining Middleware

`config.ini` can also contain middleware definitions. Middleware can be specifies for Text-to-Speech or Speech-to-Text, or both, and is executed in the order specified by `middleware` in `config.yml` just before the respective function of ModVA.

Implementation is very similar for both types of middleware. They are specified as `@stt` and `@tts` in a `commands.ini` file, with only `impl_file` and `impl_fn` specified. They are passed one argument each, containing the previous value (either from the last middleware or directly from ModVA), and return a new value to be either uttered or processed, depending on the command.

## @init

The last possible function specified in `config.ini` is `@init`. This function, like middleware, is only given `impl_file` and `impl_fn`. It is passed no parameters and is called before ModVA begins listening for commands. `@init` can be used for initialization or file management.

# Running ModVA

Once you have created modules, or just to run ModVA as it is, [Python](https://www.python.org/) must first be installed on the system. Additionally, pip should be installed with

```
> python -m ensurepip --upgrade
```

To install all required modules:

```
> pip install txtai[pipeline] SpeechRecognition sounddevice configparser importlib python-dotenv typing word2number
```

Finally, to run ModVA, use the command

```
> python Listener.py
```
