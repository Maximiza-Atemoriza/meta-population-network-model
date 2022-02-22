# Meta Population Network Model

## Setup

### Poetry

After cloning or downloading the repository we need to set up a package manager to handle our dependencies, we choose Poetry for this task. You can install Poetry [here](https://python-poetry.org/docs/) and learn how to use it [here](https://python-poetry.org/docs/basic-usage/).

Finally the project root run the following command:

```bash
make poetry # This will install dependencies and run the server
```

### Docker

To build the docker image _docker_ and _docker-compose_ are needed.

Once installed in your system execute:

```bash
make docker # This will build the docker image and start a container from it
```

### Python

Using only python. Install dependencies with:

```bash
pip3 install -r requirements.txt
```

Execute with:

```bash
python ./src/index.py
```
