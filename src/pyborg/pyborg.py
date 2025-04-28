#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File    : pyborg
Author  : A. Dareau

Comments:
"""
# %% Imports
# std library
import sys
import wave
import array
import os
from pathlib import Path

# external dependencies
import typer
from typing_extensions import Annotated

# %% Help string

HELP_STRING = """
[DELOOP]

a command line tool to deloop samples generated with the SP-404 looper
(but could work with other kind of loopers)

Usage :
   $> deloop fileA.wav fileB.wav output.wav
"""


# %% Main
import typer

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def hello():
    print("hello")


@app.command()
def goodbye():
    print("goodbye")
