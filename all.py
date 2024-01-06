#!/usr/bin/env python3

"""A script to update my stream labels"""

from effort_remaining import write_ttl
from current_task import write_in_progess


if __name__ == "__main__":
    write_in_progess()
    write_ttl()
