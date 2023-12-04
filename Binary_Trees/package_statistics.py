#!/usr/bin/python3
from __future__ import annotations  # For annotating static class methods that return a class instance

# RJ's Canonical Tech Assessment Solution
# Copyright (C) 2023  MolarFox

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from argparse import ArgumentParser, BooleanOptionalAction

import gzip
from ftplib import FTP, all_errors
from typing import Optional, Callable
from abc import ABC, abstractmethod, abstractproperty
from collections import Counter
from dataclasses import dataclass
from io import BytesIO

MIRROR = "ftp.uk.debian.org"
REPO_PATH = "/debian/dists/stable/main/"

"""A note on FTP modes and LIST cmd responses
I had some trouble getting passive mode to work, even with all the NAT rules and port forwarding rules setup on my local network for it to work.
Somehow active mode worked much more reliably, even without those rules (I suspect in part becuase my router is NAT aware of the FTP traffic?)
Anyways, this program runs in active FTP mode by default since that seems more reliable, but can be toggled using cli args!

Since the output from LIST for any FTP server is pretty much arbitrary to what the server feels like, it seemed appropriate to implement an
    accordingly adaptable interface. The intent is that if this were a real project, DirEntry could be subclassed again for any new server LIST resp formats.

(Also why nlst is probably preferable to dir, but again seemingly not as reliable on all servers now that plain FTP is a bit of a relic)
"""

def extract_architectures(listing: list[str]) -> dict[str, str]:
    """Extract the filepaths and architectures of content index files found in the output of a Mirror.ls() call

    Args:
        listing (list[str]): A list of filenames, intended to come from a Mirror.ls() call

    Returns:
        dict[str, str]: A dict where the keys are the architecture of the content index file, and the values are the filenames
    """
    archs = {}
    for filename in listing:
        if not filename.startswith("Contents"):
            continue

        # Filename may contain hash info, depending on ftp LIST wrapper method used - strip it here
        filename = filename.split('->')[0].strip()

        # Documentation guarantees contents index will always be *.gz compressed plaintext
        arch_key = filename.lstrip("Contents-").rstrip(".gz")
        archs[arch_key] = filename

    return archs


def print_valid_archs(content_files: dict[str, str]) -> None:
    """From the dict of content index files generated in `extract_architectures`, print the architectures available

    Args:
        content_files (dict[str, str]): A dict where keys are valid architectures. Vals are unused.
    """
    for arch in content_files.keys():
        print(f"  - {arch}")


def parse_content_index_entry(line_raw: str) -> Optional[tuple[str]]:
    """Attempt to parse a record in a content index file. If it appears to be invalid, return None

    Args:
        line_raw (str): _description_

    Returns:
        Optional[tuple[str]]: tuple of format (filepath, package). None if line is not valid record
    """
    if ' ' not in line_raw:
        return
    # I wasn't able to find an example of a mirror index file with lines of freeform text at the start, as per the spec
    # As a result, our only known condition for a valid line is that is must have a space in it, to delineate the two columns
    # Aside from this we likely shouldn't make any further assumptions about format without an example
    line = list(filter(lambda x: x.strip(), line_raw.split(' ')))
    return tuple(line)

@dataclass
class DirEntry(ABC):
    """Representation of the data provided per record in the response of an FTP LIST response"""
    filename: str

    @abstractmethod
    def from_list_line(cls, line: str) -> DirEntry:
        ...


@dataclass
class UnixDirEntry(DirEntry):
    """Representation of the standard UNIX LIST response format, seen for all Debian FTP host mirrors"""
    perm_triad: Optional[str] = None
    link_count: Optional[int] = None
    owner: Optional[str] = None
    group: Optional[str] = None
    size_bytes: Optional[str] = None
    mod_time: Optional[str] = None
    create_time: Optional[str] = None

    @classmethod
    def from_list_line(cls, line: str) -> DirEntry:
        """For a given record / line in an FTP LIST response that looks UNIX-like, parse it into a UnixDirEntry instance"""
        partitioned = [word for word in line.split(' ') if word]
        return cls(
            perm_triad  = partitioned[0],
            link_count  = partitioned[1],
            owner       = partitioned[2],
            group       = partitioned[3],
            size_bytes  = partitioned[4],
            mod_time    = partitioned[5:8],
            filename    = " ".join(partitioned[8:]),    # Filename may contain whitespace, hence last to proc
        )


@dataclass
class DirListing:
    """Contains a list of DirEntry instances"""
    entries: list[DirEntry]

    @staticmethod
    def parse_list_lines(lines: list[str], parser_class: DirEntry) -> DirListing:
        return DirListing(
            [parser_class.from_list_line(x) for x in lines]
        )

    def __iter__(self):
        for entry in self.entries:
            yield entry

    def filenames(self) -> list[str]:
        return [x.filename for x in self]


class Mirror:
    def __init__(self, url: str):
        self.ftp = FTP(url, user="anonymous")
        self.ftp.set_pasv(False)
        self.ftp.connect()
        self.ftp.login()

    def set_debug_level(self, new_level: int) -> None:
        """Set FTP debug level"""
        self.ftp.set_debuglevel(new_level)

    def get_debug_level(self) -> int:
        """Get FTP debug level"""
        return self.ftp.debugging

    def set_passive_mode(self, state: bool) -> None:
        """Set passive mode state"""
        self.ftp.set_pasv(state)

    def get_passive_mode(self) -> bool:
        """Get passive mode state"""
        return self.ftp.passiveserver

    def connect(self) -> None:
        """(Re-)initialise connection"""
        self.ftp.connect()
        self.ftp.login()

    def read(self, path: str, gzip_unzip: False) -> bytes:
        """Download the file at the specified path into memory as raw bytes.
            Optionally gzip decompress the file (explicitly set via flag, not inferred from extension)

        Args:
            path (str): Path to desired file on target FTP server
            gzip_unzip (False): Flag that attempts to gzip decompress the data before returning, if True

        Returns:
            bytes: Raw bytes representing the contents of the target file, optionally gzip decompressed.
        """
        file_stream = BytesIO()
        self.ftp.retrbinary(f'RETR {path}', file_stream.write)
        file_stream.seek(0)     # Reset stream head ptr to start of stream

        if gzip_unzip:
            return gzip.decompress(file_stream.read())
        return file_stream.getvalue()

    def ls(self, path: Optional[str] = None) -> list[str]:
        """Get list of files and dirs at `path`. Uses current working dir if no path specified

        Args:
            path (Optional[str], optional): Path to list files at. Defaults to None.

        Returns:
            list[str]: List of files at path (or current working dir)
        """
        if path:
            self.ftp.cwd(path)

        # Try nlst, then fallback to dir
        try:
            return self._ls_nlst_()
        except all_errors as e:
            print(f"[!] Encountered a server error while attempting nlst call. Will attempt LIST call.\n    Error detail: {e}\n")

        try:
            return self._ls_dir_().filenames()
        except all_errors as e:
            print(
                "[!] Encountered a server error while attempting LIST call. Please check your network settings, and that the server is currently up.\n"
                f"    Error detail: {e}\n"
            )
        return []

    def _ls_dir_(self) -> DirListing:
        """Retrieve directory listing using `dir`. This invisibly calls LIST and just returns the server resp (see note above)"""
        def ftp_curry(cache: list) -> Callable[[any], list[any]]:
            return lambda x: cache.append(x)

        dir_lines = []
        ftp_acc = ftp_curry(dir_lines)
        self.ftp.dir(ftp_acc)

        return DirListing.parse_list_lines(
            dir_lines,
            UnixDirEntry
        )

    def _ls_nlst_(self) -> list[str]:
        """Retrieve directory listing using `nlst` (if supported by server)"""
        return self.ftp.nlst()


def top_n_packages_by_files(index_data: Union[bytes, str], n: int = 10) -> list[tuple[str, int]]:
    """Given the raw bytes or decoded string of a content index file, determine the top n packages by file quantity

    Args:
        index_data (Union[bytes, str]): contents of index file, as raw bytes or string
        n (int, optional): Top n packages to collect. Defaults to 10.

    Returns:
        list[tuple[str, int]]: A list of the top n packages, where the tuple is of form: (<package_name>, <occurances>)
    """
    package_count = Counter()
    index_txt = index_data.decode('utf-8') if isinstance(index_data, bytes) else index_data

    for i, raw_line in enumerate(iter(index_txt.splitlines())):
        if not (line := parse_content_index_entry(raw_line)):
            print(f"[!] Found potentially invalid entry on line {i}. Skipping...")
            continue
        for p in line[-1].split(','):   # Split list of packages in rhs column
            package_count[p] += 1
    return package_count.most_common(n)


def parse_args() -> dict:
    parser = ArgumentParser(
        description="Retrieve statistics about packages for a given architecture"
    )
    parser.add_argument("arch", help="Architecture to retrieve statistics for")
    parser.add_argument(
        "-v", "--verbose",
        default=0,
        choices=[0, 1, 2],
        type=int,
        required=False,
        help="Set ftp loglevel. 0 is silent, 2 is loudest setting."
    )
    parser.add_argument(
        "-n", "--top-n",
        default=10,
        type=int,
        required=False,
        help="Choose how many of the top packages in this criteria are outputted. Defaults to 10"
    )
    parser.add_argument(
        "--passive-mode",
        action=BooleanOptionalAction,
        default=False,
        help="Run FTP operations in passive mode. Try this if encountering connection / socket issues."
    )

    return parser.parse_args()


def main():
    # Collect args, init ftp wrapper for mirror
    args = parse_args()
    mirror = Mirror(MIRROR)
    mirror.set_debug_level(args.verbose)
    mirror.set_passive_mode(args.passive_mode)

    # Collect dict of available architectures (keys), and their filepaths (vals)
    content_files = extract_architectures(mirror.ls(REPO_PATH))

    if not content_files:
        print("[!] No files were found. Please note any errors above, and retry.")
        exit(1)

    # Print the list of available architectures if an invalid one was passed through argv
    if args.arch not in content_files:
        print(f'Content file not available for architecture "{args.arch}". Available options:')
        print_valid_archs(content_files)
        exit(1)

    # Read in the relevant content index file via ftp, gzip decompress in-memory, and decode bytes to utf-8 str
    index_data = mirror.read(content_files[args.arch], gzip_unzip=True)

    # Print and exit
    print(f"Top {args.top_n} packages by number of associated files:")
    for i, package in enumerate(top_n_packages_by_files(index_data, args.top_n)):
        print(f"  {i+1:>3}: [{package[1]:>5}] {package[0]}")
    print()
    return 0


if __name__ == "__main__":
    main()
