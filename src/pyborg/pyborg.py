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
from rich import print

# % GLOBAL

# configuration files
CONFIG_DIR = Path.home() / ".config" / "pyborg"
PROFILES_FILE = CONFIG_DIR / "profiles.cfg"

# display
HEADER = ". [green]{}[/green]\n"
PARAM = "  ├── {} : {}\n"
LPARAM = "  └── {} : {}\n"

# % DEFINE APP

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True
)


# % DEFINE COMMANDS


@app.command()
def profiles(
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="show profiles settings")
    ] = False,
):
    "Lists available borg profiles"
    # -- check if config file exists
    if not PROFILES_FILE.is_file():
        msg = f"Cannot find the profile config file at '{PROFILES_FILE}'. "
        msg += "You can initialize a config file using `pyborg init`."
        print(msg)
        raise typer.Abort()

    # -- load config
    config = configparser.ConfigParser(interpolation=None)
    config.read(PROFILES_FILE)

    # -- print title
    msg = " 📄 List of Backup Profiles "
    n = len(msg) + 1
    print("╭" + "─" * n + "╮")
    print(f"│[bold blue]{msg}[/bold blue]│")
    print("╰" + "─" * n + "╯")

    # -- print profiles
    for s in config.sections():
        info = HEADER.format(s)
        if verbose:
            out = []
            for param, value in config[s].items():
                out.append(PARAM.format(param, value))
            out.pop()
            out.append(LPARAM.format(param, value))
            info += "".join(out)
        print(info)


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
        "description": "Save Important in ovh-sbg",
        "sudo": False,
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
