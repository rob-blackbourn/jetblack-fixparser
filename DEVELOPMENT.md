# Development

## Setup

1. Clone the project

2. Create the virtual environment.

    For Linux and Mac-OS.

    ```bash
    python -m venv .venv
    . .venv/bin/activate
    ```

    For windows.

    ```cmd
    python -m venv venv
    venv/Scripts/activate
    ```

3. Update pip and install build and twine in the virtual environment.
    Install the requirements for testing.

    ```bash
    pip install --upgrade pip
    pip install -r requirements-dev.txt
    ```

4. Install the project locally.

    ```bash
    pip install --editable .
    ```

## Publishing

1. Clean the build folder and build the package.

    ```bash
    rm dist/*
    python -m build
    ```

2. Publish the package.

    ```bash
    twine upload dist/*
    ```
