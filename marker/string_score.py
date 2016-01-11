#!/usr/bin/env python
# -*- coding: utf-8 -*-
# stringslipper.py: Quicksilver-like string scoring.
# Copyright (C) 2010 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright (C) 2009 Joshaven Potter <yourtech@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

def first_valid_index(a, b):
    min_index = min(a, b)
    if min_index > -1:
        return min_index
    return max(a, b)

def score(string, abbreviation):
    """
    Doctests:
    # Exact match
    >>> assert score("Hello world", "Hello world") == 1.0

    # Not matching
    >>> assert score("Hello world", "hellx") == 0   # non-existent character in match should return 0
    >>> assert score("Hello world", "hello_world") == 0  # non-existent character in match should return 0

    # Match must be sequential
    >>> assert score("Hello world", "WH") == 0
    >>> assert score("Hello world", "HW") > 0

    # Same case should match better than wrong case
    >>> assert score("Hello world", "hello") < score("Hello world", "Hello")

    # FAIL: Closer matches should have higher scores
    # score("Hello world", "H") < score("Hello world", "He")
    # True

    # Should match first matchable character regardless of case
    >>> score("Hillsdale Michigan", "himi") > 0
    True

    # Advanced scoring methods
    # Consecutive letter bonus
    >>> score("Hello World", "Hel") > score("Hello World", "Hld")
    True

    # Acronym bonus
    >>> score("Hello World", "HW") > score("Hello World", "ho")
    True
    >>> score("yet another Hello World", "yaHW") > score("Hello World", "yet another")
    True

    # score("Hillsdale Michigan", "HiMi") > score("Hillsdale Michigan", "Hil")
    # True

    >>> score("Hillsdale Michigan", "HiMi") > score("Hillsdale Michigan", "illsda")
    True
    >>> score("Hillsdale Michigan", "HiMi") > score("Hillsdale Michigan", "hills")
    True

    # Beginning of string bonus
    >>> score("Hillsdale", "hi") > score("Chippewa", "hi")
    True

    # Proper string weights
    >>> score("Research Resources North", "res") > score("Mary Conces", "res")
    True
    >>> score("Research Resources North", "res") > score("Bonnie Strathern - Southwest Michigan Title Search", "res")
    True

    # Start of string bonus
    >>> score("Mary Large", "mar") > score("Large Mary", "mar")
    True
    >>> score("Silly Mary Large", "mar") == score("Silly Large Mary", "mar")
    True

    # Examples
    >>> assert score("hello world", "ax1") == 0
    >>> assert score("hello world", "ow") > 0.14
    >>> assert score("hello world", "h") >= 0.09
    >>> assert score("hello world", "he") >= 0.18
    >>> assert score("hello world", "hel") >= 0.27
    >>> assert score("hello world", "hell") >= 0.36
    >>> assert score("hello world", "hello") >= 0.45

    >>> assert score("hello world", "helloworld") >= 0.5   # FAIL: Not 0.9 JS
    >>> assert score("hello world", "hello worl") >= 0.5   # FAIL: Not 0.9 JS
    >>> assert score("hello world", "hello world") == 1

    >>> assert score("Hello", "h") >= 0.13
    >>> assert score("He", "h") > 0.35

    # Same case matches better than wrong case.
    >>> assert score("Hello", "h") >= 0.13
    >>> assert score("Hello", "H") >= 0.2

    # FAIL: Acronyms are not given more weight.
    # assert score("Hillsdale Michigan", "HiMi") > score("Hillsdale Michigan", "Hills")
    # assert score("Hillsdale Michigan", "Hillsd") > score("Hillsdale Michigan", "HiMi")
    """
    if string == abbreviation or not abbreviation:
        return 1.0

    total_character_score = 0
    start_of_string_bonus = False
    abbreviation_length = len(abbreviation)
    string_length = len(string)

    # Walk through the abbreviation and add up scores.
    for i, c in enumerate(abbreviation):
        # Find the first case-insensitive match of a character.
        c_lower = c.lower()
        c_upper = c.upper()
        index_in_string = first_valid_index(string.find(c_lower), string.find(c_upper))

        # Bail out if the character is not found in string.
        if index_in_string == -1:
            return 0

        # Set base score for matching 'c'.
        character_score = 0.09

        # Case bonus
        if string[index_in_string] == c:
            character_score += 0.09

        # Consecutive letter and start of string bonus.
        if not index_in_string: # 0 == index_in_string
            # increase the score when matching first char of the remainder of the string.
            character_score += 0.79
            # If the match is the first letter of the string and first letter of abbr.
            if not i: # 0 == i
                start_of_string_bonus = True

        # Acronym bonus
        if string[index_in_string - 1] == ' ':
            character_score += 0.79 # * Math.min(index_in_string, 5); # cap bonus at 0.4 * 5

        # Only remaining substring will be searched in the next iteration.
        string = string[index_in_string+1:]

        # Add up score.
        total_character_score += character_score

    # Uncomment to weigh smaller words higher.
    # return total_character_score / string_length

    abbreviation_score = total_character_score / abbreviation_length
    percentage_of_matched_string = abbreviation_length / string_length
    word_score = abbreviation_score * percentage_of_matched_string
    final_score = (word_score + abbreviation_score)/2 # softens the penalty for longer strings.
    if start_of_string_bonus and (final_score + 0.09 < 1):
        final_score += 0.09
    return final_score
