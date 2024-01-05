#!/usr/bin/env python3

"""A script to update my stream labels"""

from inprogress import write_ttl
from launch_when import write_in_progess


if __name__ == "__main__":
    write_in_progess()
    write_ttl()
