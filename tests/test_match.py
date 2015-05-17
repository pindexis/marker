import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from marker.core import Mark,Bookmarks

def _equals(marks_list1, marks_list2):
	l1 = sorted(marks_list1)
	l2 = sorted(marks_list2)
	if len(l1) != len(l2):
		return False
	for i,_ in enumerate(l1):
		if l1[i] != l2[i]:
			return False
	return True

m_cd = Mark('cd path/to/nowhere','gotonowhere')
m_tar = Mark('tar -cvf','')
m_grep = Mark('grep -irn', None)
m_untar = Mark('tar -xvf','Untar')

bookmarks_data = [m_cd, m_tar, m_grep, m_untar]

bookmars = Bookmarks(bookmarks_data)

def test_match_empty():
	assert(_equals(bookmars.get_matches(""), bookmarks_data))

def test_match_character():
	assert(_equals(bookmars.get_matches("c"), [m_cd, m_tar]))

def test_match_word():
	assert(_equals(bookmars.get_matches("tar"), [m_tar, m_untar]))

def test_match_multi_word():
	assert(_equals(bookmars.get_matches("tar c"), [m_tar]))	

def test_match_alias():
	assert(_equals(bookmars.get_matches("Untar"), [m_untar]))

def test_match_alias():
	assert(_equals(bookmars.get_matches("cd goto"), [m_cd]))

def test_match_double():
	assert(_equals(bookmars.get_matches("grep grep"), []))
	assert(_equals(bookmars.get_matches("grep grep -"), []))
	assert(_equals(bookmars.get_matches("tar tar"), [m_untar]))

def test_match_case():
	assert(_equals(bookmars.get_matches("untar"), [m_untar]))
	assert(_equals(bookmars.get_matches("UNTAR"), [m_untar]))

def test_spaces():
	assert(_equals(bookmars.get_matches(" "), bookmarks_data))
	assert(_equals(bookmars.get_matches("   grep     "), [m_grep]))
	assert(_equals(bookmars.get_matches("tar     Untar   "), [m_untar]))
