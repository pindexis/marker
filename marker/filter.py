from . import string_score
import re

def filter_commands(marks, search_string):
    ''' return the list of marks that match a given search string
     A mark is considered a match if:
       - all words in the search string except the last one must have exact match, meaning they are present in either the command or the alias
       - for the last word, it can be contained in any word in the command or alias
     For example: 'cd tonowhere' will match 'c','cd n' but not 'c ', 'c t'
    '''
    def sort_marks(marks, search_string):
        return sorted(
                marks,
                key=lambda m:(string_score.score(m.cmd, search_string)*2 + string_score.score(m.alias, search_string)),
                reverse=True
                )
    def contained(candidate, container):
        tmp = container[:]
        try:
            for i, word in enumerate(candidate):
                if i == len(candidate) - 1:
                    if any(word in c for c in tmp):
                        return True
                    else:
                        return False
                else:
                    tmp.remove(word)
        except ValueError:
            return False
    # Remove extra spaces
    # keep a space if it is at the end of string, since it means that a whole word must be matched
    search_string = search_string.lstrip()
    if not search_string:
        return sort_marks(marks, "")

    filtered_bookmarks = []
    words_re = re.compile('\w+')
    search_words = words_re.findall(search_string.lower())
    for mark in marks:
        mark_splitted = words_re.findall(mark.cmd.lower()) + words_re.findall(mark.alias.lower())
        if contained(search_words, mark_splitted):
            filtered_bookmarks.append(mark)

    return sort_marks(filtered_bookmarks, search_string)
