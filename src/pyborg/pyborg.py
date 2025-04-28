#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File    : pyborg
Author  : A. Dareau

Comments:
"""

# % IMPORTS

# std library
import sys
import configparser
from pathlib import Path


# external dependencies
import typer
from typing_extensions import Annotated

# % GLOBAL
CONFIG_DIR = Path.home() / ".config" / "pyborg"
PROFILES_FILE = CONFIG_DIR / "profiles.cfg"

# % DEFINE APP

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True
)


# % DEFINE COMMANDS


@app.command()
def profiles():
    "Lists available borg profiles"
    print("hello")


@app.command()
def list(profile: str):
    print("goodbye")


@app.command(rich_help_panel="Configs")
def init():
    """
    [blue]Initializes[/blue] the profile config file.
    """
    # - create config dir
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()

    # - ask confirmation if already profile
    if PROFILES_FILE.is_file():
        msg = f"There is already an existing profile file at '{PROFILES_FILE}', overwrite it ?"
        overwrite = typer.confirm(msg)
        if not overwrite:
            print("Do not overwrite...")
            raise typer.Abort()
        print("Overwriting the file !")

    # - create default config
    config = configparser.ConfigParser(interpolation=None)
    config["example"] = {
        "sudo": False,
        "description": "Save Important in ovh-sbg",
        "source": "/path/to/backup/source",
        "repository": "/path/to/borg/repo",
        "save_fmt": r"{now:%Y-%m-%d_%H:%M:%S}_{hostname}",
        "option": "--exclude-from ~/.config/pyborg/.borg-exclude",
        "compression": "lz4,7",
    }

    with PROFILES_FILE.open("+w") as f:
        config.write(f)

    # - print success
    print("Example config file created !")
    print(f">> {PROFILES_FILE}")
