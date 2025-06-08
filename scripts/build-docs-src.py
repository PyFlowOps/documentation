# This script builds the /src directory for the documentation.
# This directory is where the site pulls it's information from
# so we want to populate it with the latest information from the repos.

import os
import shutil
import argparse
import subprocess
import sys
import random
import time
import yaml

from icecream import ic
from termcolor import colored
from halo import Halo
from functools import wraps

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_url = "https://github.com/PyFlowOps"
_dest = os.path.abspath(os.path.join(BASE, "docs", "src"))
_temp = os.path.abspath(os.path.join(BASE, "temp"))

os.system('cls' if os.name == 'nt' else 'clear') # Clear the console

ic.disable() # Disable icecream output

# Setting the Halo spinner for the console output
spinner = Halo(spinner="dots") # Spinner for the console output
spinner.info("🌐 Building the Documentation Site and Prepping for Deployment...") # Start the spinner

# Check if the temp directory exists, if it does, delete it and create a new one
if os.path.exists(_temp):
    shutil.rmtree(_temp)
    os.makedirs(_temp)
else:
    os.makedirs(_temp)

_cfg_file = os.path.abspath(os.path.join(BASE, "site-config.yml")) # The config file for the docs - in the root of the repo


def advanced_spinner(text="Processing...", success="✅ Done!", fail="❌ Failed!"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            spinner = Halo(text=text, spinner='dots')
            spinner.start()
            try:
                result = func(*args, **kwargs)
                spinner.succeed(success)
                return result
            except Exception as e:
                spinner.fail(fail)
                raise e
        return wrapper
    return decorator


@advanced_spinner(
    text="⚙️ Cleaning up the src directory...",
    success="🎉 Cleaned up the src directory!",
    fail="🔥 Failed to clean up the src directory!"
)
def _clean():
    if os.path.isdir(os.path.join(BASE, "site")):
        ic("Removing directory: ", os.path.join(BASE, "site"))
        shutil.rmtree(os.path.join(BASE, "site"))

    for _repo in _config["repos"]:
        for k, _ in _repo.items():
            if os.path.isdir(os.path.join(_dest, k)):
                if os.path.isdir(os.path.join(_dest, "docker")):
                    ic("Removing directory: ", os.path.join(_dest, "docker"))
                    shutil.rmtree(os.path.join(_dest, "docker"))

                # If the directory exists, remove it
                ic("Removing directory: ", os.path.join(_dest, k))
                shutil.rmtree(os.path.join(_dest, k))
                time.sleep(.5)


def clone_repos():
    for _repo in _config["repos"]:
        for k, v in _repo.items():
            Halo(spinner='dots').start()
            # The key is the name of the repo
            _repo_to_clone = f"{_url}/{k}"
            _temp_dir = os.path.join(_temp, k)
            ic(f"Cloning {_repo_to_clone} to {_temp_dir}")
            _cmd = [
                "git",
                "clone",
                "--quiet",
                "--branch",
                "main",
                _repo_to_clone,
                _temp_dir
            ]
            
            # Clone the repo to the temp directory
            try:
                subprocess.run(_cmd, cwd=_temp, check=True)
            except subprocess.CalledProcessError as e:
                Halo(text=f"Cloning Repository {k}", spinner='dots').fail()

            Halo(text=f"⬇️  Cloning Repository {k}", spinner='dots').succeed()


def _copy_contents(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)  # Create destination directory if it doesn't exist

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dst_path)


def _copy_dir(src, dst):
    """
    Copy DIRECTORY src to dst

    Example:
    src: /home/user/repo/src
    dst: /home/user/repo/docs/src
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)

    shutil.copytree(src, dst)


def _copy_file(src, dst):
    """
    Copy the file src to dst

    Example:
    src: /home/user/repo/src/file.txt
    dst: /home/user/repo/docs/src/file.txt
    """
    # Let's create the destination directory if it doesn't exist - for README.md or pulls that require no directories
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    if os.path.isfile(dst):
        os.remove(dst)
    
    # Copy the file
    shutil.copy(src, dst) # Copy the file to the destination directory


def build_docs_site():
    for _repo in _config["repos"]:
        for _repo, _repo_data in _repo.items():
            if not isinstance(_repo_data, dict):
                Halo(text=colored(f"⚠️  `{_repo}` is not a valid configuration, please review the configuration file. ⚠️", "yellow", attrs=["bold"]), spinner='dots', color='yellow').warn()
                continue

            if "directories" not in _repo_data:
                Halo(text=colored(f"⚠️  There are no directories in `{_repo}` to copy, this could cause an issue with links, etc. ⚠️", "yellow", attrs=["bold"]), spinner='dots', color='yellow').warn()
                _directories_to_copy = [] # Set an empty list
            else:
                _directories_to_copy = _repo_data["directories"] # The directories to copy

            if not "files" in _repo_data:
                Halo(text=colored(f"⚠️  There are no files in `{_repo}` to copy, this could cause an issue with links, etc. ⚠️", "yellow", attrs=["bold"]), spinner='dots', color='yellow').warn()
                _files_to_copy = [] # Set an empty list
            else:
                _files_to_copy = _repo_data["files"] # The files to copy

            __source_dir = os.path.join(_temp, _repo) # The source directory /temp/<repo_name>
            __dest_dir = os.path.join(_dest, _repo) # The destination directory /docs/src/<repo_name>

            # Debugging output
            ic(" -- Data Integrity Check --")
            ic("Source Directory: ", __source_dir)
            ic("Destination Directory: ", __dest_dir)
            ic("Directories to copy: ", _directories_to_copy)
            ic("Files to copy: ", _files_to_copy)

            Halo(spinner='dots').start() # Start the spinners
            try:
                if _directories_to_copy:
                    for package in _directories_to_copy:
                        ic(f"Current Package -- {package}") # Debugging output
                        for _dir, _data in package.items():
                            # These are the 'directories' in the sre-docs-config.yml to copy
                            if "subdir" in _data:
                                if _data["contents_only"] == True:
                                    _src_dir = os.path.join(_temp, _repo, _dir) # The source directory /temp/<repo_name>/<dir>
                                    _dest_dir = os.path.join(_dest, _data["subdir"], _repo) # The destination directory with the subdir /docs/src/<subdir>
                                    ic("Copying directory contents: ", __source_dir, " to ", _dest_dir) # Debugging output
                                    _copy_contents(_src_dir, _dest_dir)
                                else:
                                    _src_dir = os.path.join(_temp, _repo, _dir)
                                    _dest_dir = os.path.join(_dest, _repo, _data["subdir"], _repo)
                                    ic("Copying directory: ", _src_dir, " to ", _dest_dir) # Debugging output
                                    _copy_dir(_src_dir, _dest_dir)
                            else:
                                if _data["contents_only"] == True:
                                    _src_dir = os.path.join(_temp, _repo, _dir)
                                    _dest_dir = os.path.join(_dest, _repo)
                                    ic("Copying directory contents: ", _src_dir, " to ", _dest_dir) # Debugging output
                                    _copy_contents(_src_dir, _dest_dir)
                                else:
                                    _src_dir = os.path.join(_temp, _repo, _dir)
                                    _dest_dir = os.path.join(_dest, _repo, _dir)
                                    ic("Copying directory: ", _src_dir, " to ", _dest_dir) # Debugging output
                                    _copy_dir(_src_dir, _dest_dir)

                # We want to move any files to the root of the destination directory
                if _files_to_copy:
                    for _file in _files_to_copy:
                        _input_file = os.path.join(_temp, _repo, _file)
                        assert os.path.exists(_input_file), f"File does not exist: {_input_file}"

                        #if "docker" in _file:
                        #    _output_file = os.path.join(_dest, _file)

                        #    ic("Copying file: ", _input_file, " to ", _output_file) # Debugging output
                        #    assert not os.path.exists(_output_file), f"File already exists: {_output_file}"
                        #    
                        #    _copy_file(_input_file, _output_file)
                        #    continue
                        
                        _output_file = os.path.join(_dest, _repo, _file)

                        assert not os.path.exists(_output_file), f"File already exists: {_output_file}"
                        
                        ic("Copying file: ", _input_file, " to ", _output_file) # Debugging output
                        _copy_file(_input_file, _output_file)
            

            except Exception as e:
                Halo(text=f"Building {_repo} -- {e}", spinner='dots').fail()

            time.sleep(random.uniform(0, 2)) # Sleep for a random time between 1 and 4 second
            Halo(text=f"🎉 Building {_repo} Complete!", spinner='dots').succeed()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Build the documentation site.")
    argparser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Run the script in debug mode. This will enable the icecream output."
    )
    args = argparser.parse_args()
    if args.debug:
        ic.enable()

    # Let's load the config file
    with open(_cfg_file, "r") as f:
        _config = yaml.safe_load(f)

    _clean() # Clean the src directory

    clone_repos() # Clone the repos
    Halo(text=f"⭐ Cloning Process Complete!").succeed()
    print("\n")

    build_docs_site() # Build the docs site
    Halo(text=f"⭐ Build Process Complete!").succeed()
    print("\n")

    spinner.info("🔧 Please Run the Local Server - `make serve`") # Start the spinner
    print("\n")
