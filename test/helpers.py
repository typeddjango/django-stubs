import inspect
import os
import re
from typing import List, Callable, Optional, Tuple

import pytest  # type: ignore  # no pytest in typeshed

skip = pytest.mark.skip

# AssertStringArraysEqual displays special line alignment helper messages if
# the first different line has at least this many characters,
MIN_LINE_LENGTH_FOR_ALIGNMENT = 5


class TypecheckAssertionError(AssertionError):
    def __init__(self, error_message: str, lineno: int):
        self.error_message = error_message
        self.lineno = lineno

    def first_line(self):
        return self.__class__.__name__ + '(message="Invalid output")'

    def __str__(self):
        return self.error_message


def _clean_up(a: List[str]) -> List[str]:
    """Remove common directory prefix from all strings in a.

    This uses a naive string replace; it seems to work well enough. Also
    remove trailing carriage returns.
    """
    res = []
    for s in a:
        prefix = os.sep
        ss = s
        for p in prefix, prefix.replace(os.sep, '/'):
            if p != '/' and p != '//' and p != '\\' and p != '\\\\':
                ss = ss.replace(p, '')
        # Ignore spaces at end of line.
        ss = re.sub(' +$', '', ss)
        res.append(re.sub('\\r$', '', ss))
    return res


def _num_skipped_prefix_lines(a1: List[str], a2: List[str]) -> int:
    num_eq = 0
    while num_eq < min(len(a1), len(a2)) and a1[num_eq] == a2[num_eq]:
        num_eq += 1
    return max(0, num_eq - 4)


def _num_skipped_suffix_lines(a1: List[str], a2: List[str]) -> int:
    num_eq = 0
    while (num_eq < min(len(a1), len(a2))
           and a1[-num_eq - 1] == a2[-num_eq - 1]):
        num_eq += 1
    return max(0, num_eq - 4)


def _add_aligned_message(s1: str, s2: str, error_message: str) -> str:
    """Align s1 and s2 so that the their first difference is highlighted.

    For example, if s1 is 'foobar' and s2 is 'fobar', display the
    following lines:

      E: foobar
      A: fobar
           ^

    If s1 and s2 are long, only display a fragment of the strings around the
    first difference. If s1 is very short, do nothing.
    """

    # Seeing what went wrong is trivial even without alignment if the expected
    # string is very short. In this case do nothing to simplify output.
    if len(s1) < 4:
        return error_message

    maxw = 72  # Maximum number of characters shown

    error_message += 'Alignment of first line difference:\n'
    # sys.stderr.write('Alignment of first line difference:\n')

    trunc = False
    while s1[:30] == s2[:30]:
        s1 = s1[10:]
        s2 = s2[10:]
        trunc = True

    if trunc:
        s1 = '...' + s1
        s2 = '...' + s2

    max_len = max(len(s1), len(s2))
    extra = ''
    if max_len > maxw:
        extra = '...'

    # Write a chunk of both lines, aligned.
    error_message += '  E: {}{}\n'.format(s1[:maxw], extra)
    # sys.stderr.write('  E: {}{}\n'.format(s1[:maxw], extra))
    error_message += '  A: {}{}\n'.format(s2[:maxw], extra)
    # sys.stderr.write('  A: {}{}\n'.format(s2[:maxw], extra))
    # Write an indicator character under the different columns.
    error_message += '     '
    # sys.stderr.write('     ')
    for j in range(min(maxw, max(len(s1), len(s2)))):
        if s1[j:j + 1] != s2[j:j + 1]:
            error_message += '^'
            # sys.stderr.write('^')  # Difference
            break
        else:
            error_message += ' '
            # sys.stderr.write(' ')  # Equal
    error_message += '\n'
    return error_message
    # sys.stderr.write('\n')


def assert_string_arrays_equal(expected: List[str], actual: List[str]) -> None:
    """Assert that two string arrays are equal.

    Display any differences in a human-readable form.
    """

    actual = _clean_up(actual)
    error_message = ''

    if actual != expected:
        num_skip_start = _num_skipped_prefix_lines(expected, actual)
        num_skip_end = _num_skipped_suffix_lines(expected, actual)

        error_message += 'Expected:\n'

        # If omit some lines at the beginning, indicate it by displaying a line
        # with '...'.
        if num_skip_start > 0:
            error_message += '  ...\n'

        # Keep track of the first different line.
        first_diff = -1

        # Display only this many first characters of identical lines.
        width = 75

        for i in range(num_skip_start, len(expected) - num_skip_end):
            if i >= len(actual) or expected[i] != actual[i]:
                if first_diff < 0:
                    first_diff = i
                error_message += '  {:<45} (diff)'.format(expected[i])
            else:
                e = expected[i]
                error_message += '  ' + e[:width]
                if len(e) > width:
                    error_message += '...'
            error_message += '\n'
        if num_skip_end > 0:
            error_message += '  ...\n'

        error_message += 'Actual:\n'

        if num_skip_start > 0:
            error_message += '  ...\n'

        for j in range(num_skip_start, len(actual) - num_skip_end):
            if j >= len(expected) or expected[j] != actual[j]:
                error_message += '  {:<45} (diff)'.format(actual[j])
            else:
                a = actual[j]
                error_message += '  ' + a[:width]
                if len(a) > width:
                    error_message += '...'
            error_message += '\n'
        if actual == []:
            error_message += '  (empty)\n'
        if num_skip_end > 0:
            error_message += '  ...\n'

        error_message += '\n'

        if 0 <= first_diff < len(actual) and (
                len(expected[first_diff]) >= MIN_LINE_LENGTH_FOR_ALIGNMENT
                or len(actual[first_diff]) >= MIN_LINE_LENGTH_FOR_ALIGNMENT):
            # Display message that helps visualize the differences between two
            # long lines.
            error_message = _add_aligned_message(expected[first_diff], actual[first_diff],
                                                 error_message)

        first_failure = expected[first_diff]
        if first_failure:
            lineno = int(first_failure.split(' ')[0].strip(':').split(':')[1])
            raise TypecheckAssertionError(error_message=f'Invalid output: \n{error_message}',
                                          lineno=lineno)


def build_output_line(fname: str, lnum: int, severity: str, message: str, col=None) -> str:
    if col is None:
        return f'{fname}:{lnum + 1}: {severity}: {message}'
    else:
        return f'{fname}:{lnum + 1}:{col}: {severity}: {message}'


def expand_errors(input_lines: List[str], fname: str) -> List[str]:
    """Transform comments such as '# E: message' or
    '# E:3: message' in input.

    The result is lines like 'fnam:line: error: message'.
    """
    output_lines = []
    for lnum, line in enumerate(input_lines):
        # The first in the split things isn't a comment
        for possible_err_comment in line.split(' # ')[1:]:
            m = re.search(
                r'^([ENW]):((?P<col>\d+):)? (?P<message>.*)$',
                possible_err_comment.strip())
            if m:
                if m.group(1) == 'E':
                    severity = 'error'
                elif m.group(1) == 'N':
                    severity = 'note'
                elif m.group(1) == 'W':
                    severity = 'warning'
                col = m.group('col')
                output_lines.append(build_output_line(fname, lnum, severity,
                                                      message=m.group("message"),
                                                      col=col))
    return output_lines


def get_func_first_lnum(attr: Callable[..., None]) -> Optional[Tuple[int, List[str]]]:
    lines, _ = inspect.getsourcelines(attr)
    for lnum, line in enumerate(lines):
        no_space_line = line.strip()
        if f'def {attr.__name__}' in no_space_line:
            return lnum, lines[lnum + 1:]
    raise ValueError(f'No line "def {attr.__name__}" found')
