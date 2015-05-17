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

def test_add():
	bookmarks = Bookmarks([])
	bookmarks.add_mark(m_cd)
	assert(_equals(bookmarks.marks, [m_cd]))
	assert(bookmarks.dirty)

def test_remove():
	bookmarks = Bookmarks([m_cd,m_tar])
	bookmarks.remove_mark(m_cd)
	assert(_equals(bookmarks.marks, [m_tar]))
	assert(bookmarks.dirty)	

def test_add_existing():
	bookmarks = Bookmarks([m_cd])
	bookmarks.add_mark(m_cd)
	assert(_equals(bookmarks.marks, [m_cd]))
	assert(not bookmarks.dirty)

def test_overwrite():
	secondMark = Mark('cd path/to/nowhere','gotosomewhere')
	bookmarks = Bookmarks([m_cd])
	bookmarks.add_mark(secondMark)
	assert(_equals(bookmarks.marks, [secondMark]))
	assert(bookmarks.dirty)	