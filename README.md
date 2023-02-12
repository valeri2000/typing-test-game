# Typing test game

This is a typing test game written in Python with multiplayer support.

## Install instructions

1. Create virtual environment and load it:

```
λ mkdir venv
λ python3 -m venv venv
λ source venv/bin/activate
λ pip install --upgrade pip
```

2. Install necessary dependencies:

    2.1. For Linux
    ```
    λ pip install -r requirements-linux.txt
    ```

    2.2. For Windows (curses package is windows-curses, **not tested**)
    ```
    λ pip install -r requirements-windows.txt
    ```

3. To start

    3.1. Configure server address and port for multiplayer functionality in src/config.py (default is **localhost:12346**)

    3.2. Execute following commands
    ```
    λ python src/server.py # single instance needed for server for multiplayer
    λ python src/main.py   # instance for the client/game, in another terminal
    ```
