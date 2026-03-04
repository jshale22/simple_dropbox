# Dropbox Example

This code has been split into two components.

## First Component

The first component (under the `first_component` directory) contains a FastAPI application that creates, updates, deletes, and lists files in a specified directory. This is determined by the config item `BASE_DIR` in the `config.toml` within this directory. You can edit this if you wish when testing, but I have set it to `/tmp/test1`. Please ensure that the directory exists before running the application; otherwise, it won't work.

It is important to note that the API may not be completely foolproof. There are likely some weaknesses, and my limited knowledge of file commands in Python contributes to this.

Once a directory has been created and set in the `config.toml` (if you have decided to change it), you must enter the `first_component` directory and build the environment using `uv`. Ensure that this has been installed using `pip install uv`. This application was created using Python 3.12.3, so it is important to be consistent. There is a Makefile that should handle this for you. Enter `make install`, and the `.venv` should be created with the necessary Python modules. You can then run `make run` to start the application. By default, it should run at `http://127.0.0.1:8000`, and you can access the docs at `http://127.0.0.1:8000/docs`.

Some other optional commands are `make test`, `make check_subset`, and `make clean`. As the first two suggest, these run simple unit tests to ensure that the code for creating, updating, deleting, and listing files works as expected. The final command, `make clean`, can be used to wipe the `.venv` and allow you to create a fresh one if desired.

## Second Component

The second component is a Python script that can be run via the command line. In another terminal, enter the `second_directory` and ensure you are still using Python 3.12.3. Run `pip install -r requirements.txt` to install the required modules, and then run:

```bash
python main.py /path/to/source --app http://127.0.0.1:8000
```
I tested this by creating a second directory under `/tmp/test2`. You can choose how to set it up, but please make sure that the directory exists beforehand.

## Final testing

Once both components are running in separate terminals, you can make changes to files in your source directory and expect them to appear in the destination directory after a certain interval (currently set to 30 seconds).

## Assumptions

Some assumptions have been made for simplicity:
1. The app only expects files to be sent for creation, updating, or deletion — it will never create a directory. This avoids overcomplicating the example and keeps it as foolproof as possible.
2. Files in the source directory are assumed to change frequently, meaning updates need to be relatively fast. This was mainly for testing purposes, which is why the interval is set to 30 seconds. For less active directories, a longer interval (e.g., 10 minutes) would suffice.
3. The second component is assumed to remain within a single file, as it is more of a script than a full application. This was done for simplicity, while the first component demonstrates a more structured setup.
