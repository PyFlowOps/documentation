#!/usr/bin/env bash
# These are functions that are used in the scripts
# This file is sourced by other scripts

set -eo pipefail

CLEAN_FOLDERS=( "docs" "temp" "docker" "iac" )

function rsync_files_usage(){
    echo "Usage: rsync_files <source_directory> <destination_directory>"
    echo "Syncs files from source_directory to destination_directory"
    echo "Example: rsync_files /path/to/source /path/to/destination"
}

function rsync_files(){
    # This is a function that does something
    [[ -z "$1" ]] && { echo "No source directory provided"; rsync_files_usage; return 1; }
    [[ -z "$2" ]] && { echo "No destination directory provided"; rsync_files_usage; return 1; }

    echo "Syncing files from directory: ${1} --> ${2}"
    [[ ! -d "${2}" ]] && mkdir -p "${2}" # Create the destination directory if it doesn't exist
    [[ ! -d "${1}" ]] && { echo "Source directory does not exist"; return 1; } # Check if source directory exists
    
    rsync -av --exclude='.git' "${1}"/* "${2}"
}

function rsync_dir(){
    [[ -z "$1" ]] && { echo "No source directory provided"; return 1; }
    [[ -z "$2" ]] && { echo "No destination directory provided"; return 1; }

    echo "Syncing directory: ${1} --> ${2}"
    [[ ! -d "${2}" ]] && mkdir -p "${2}" # Create the destination directory if it doesn't exist
    [[ ! -d "${1}" ]] && { echo "Source directory does not exist"; return 1; } # Check if source directory exists
    rsync -av --exclude='.git' "${1}" "${2}"
}

function copy_file(){
    # This is a function that does something
    [[ -z "$1" ]] && { echo "No file provided"; return 1; }
    [[ -z "$2" ]] && { echo "No search string provided"; return 1; }

    dest_filename=$(dirname "${2}") # This is the destination directory

    echo "Copy file: ${1} --> ${2}"
    echo "Ensure destination directory exists --> ${dest_filename}"
    [[ ! -d "${dest_filename}" ]] && mkdir -p "${dest_filename}" # Create the destination directory if it doesn't exist
    [[ ! -f "${1}" ]] && { echo "Source file does not exist --> ${1}"; return 1; } # Check if source file exists
    [[ -f "${2}" ]] && { echo "File found -- syncing..."; rsync -av "${1}" "${2}"; } # Remove the source file if it exists
    [[ ! -f "${2}" ]] && cp -R "${1}" "${2}" # Copy the file to the new location
    echo "Copying file: ${1} --> ${2}"
}

function clean(){
    # Cleaning the docs folder
    for i in "${CLEAN_FOLDERS[@]}"; do
        if [[ -d "${BASEDIR}/docs/src/${i}" ]]; then
            rm -rf "${BASEDIR}/docs/src/${i}"
        fi
    done
}
