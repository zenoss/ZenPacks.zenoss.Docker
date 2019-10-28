##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Parsing helpers for docker command line output."""

import re


class MissingColumnsError(Exception):
    def __init__(self, message, expected=None, found=None, data=None):
        self.expected = expected
        self.found = found
        self.data = data


class CgroupPathNotFound(Exception):
    pass


def rows_from_output(output, expected_columns=None):
    """Return list of table row dicts given command output.

    Raises MissingColumnsError if expected_columns is specified, and any of the
    column names in that iterable are not found in output.

    See tests/test_parsing for example values for args and return.

    """
    rows = []

    lines = output.strip().splitlines()
    if not lines:
        if expected_columns:
            raise MissingColumnsError(
                "empty data",
                expected=expected_columns,
                found=[],
                data=output)

        return []

    header_line = lines[0]
    row_lines = lines[1:]

    columns = re.split(r' {2,}', header_line)

    if expected_columns:
        if not set(expected_columns).issubset(columns):
            raise MissingColumnsError(
                "missing columns in data",
                expected=expected_columns,
                found=columns,
                data=output)

    column_indexes = {
        c: (
            header_line.find(c),
            header_line.find(columns[i + 1]) if i + 1 < len(columns) else None)
        for i, c in enumerate(columns)}

    for line in row_lines:
        rows.append({
            column: line[start:end].strip()
            for column, (start, end) in column_indexes.items()})

    return rows


def cgroup_path_from_output(output):
    """Return mounted path to cgroup given the content of /proc/self/mountinfo.

    Raises CgroupPathNotFound if the path to cgroup is not found in the file.
    """
    lines = output.strip().splitlines()
    if not lines:
        raise CgroupPathNotFound()

    try:
        for line in lines:
            fields = line.split(' ')
            if 'cgroup' in fields[4]:
                mount_path = fields[4]
                index = mount_path.find('cgroup')
                mount_path = mount_path[:index] + 'cgroup'

                return mount_path
    except IndexError:
        pass

    raise CgroupPathNotFound()
