import os
import subprocess
from decouple import config
from typing import List

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXTRACT_SH_PATH = os.path.join(BASE_PATH, config("BASH_SCRIPT_NAME"))


def subprocess_run(argument: List[str]) -> str:
    """_summary_
           This runs a bash script in a subprocess based on on the input arguments
    Args:
        argument (List[str]): takes list of string arguments

    Returns:
        str: output from bash run
    """
    arguments = argument

    return subprocess.run(
        ["bash", EXTRACT_SH_PATH, *arguments],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
