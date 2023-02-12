# Typing test game

This is a typing test game written in Python with multiplayer support (maximum of 1 game at a time consisting of 2 players)

## Install instructions

1. Create virtual environment and load it:

```
λ mkdir venv
λ python -m venv venv
λ source venv/bin/activate (venv\Scripts\activate.bat for Windows)
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

3. To start:

    3.1. Configure server address and port for multiplayer functionality in src/config.py (default is **localhost:12346**)

    3.2. Execute following commands:
    ```
    λ python src/server.py (src\server.py for Windows) # single instance needed for server for multiplayer
    λ python src/main.py (src\main.py for Windows)     # instance for the client/game, in another terminal
    ```
    
    3.3. To execute tests:
    ```
    λ python src/utils_test.py (src\utils_test.py for Windows)
    ```
    
