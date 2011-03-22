# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
# ***** BEGIN LICENCE BLOCK *****
#
# The Initial Developer of the Original Code is
# The Northeastern University CCIS Volunteer Systems Group
#
# Contributor(s):
#   Alex Lee <lee@ccs.neu.edu>
#
# ***** END LICENCE BLOCK *****

import os
import threading
import time
import urlparse
import posixpath


def module(file_path):
    """Returns the module name.
    >>> module('/a/b/c/xx.py')
    'c'
    """
    dir = os.path.dirname(file_path)
    dir_abs = os.path.abspath(dir)
    dir_norm = os.path.normpath(dir_abs)
    return dir_norm.split(os.sep)[-1]


def root(file_path):
    """Returns a 'lambda' that produces paths based on the given file_path.
    >>> x = root('/a/b/c/xx.py')
    >>> x('t')
    '/a/b/c/t'
    >>> x('t', 's')
    '/a/b/c/t/s'
    """
    dir = os.path.dirname(file_path)
    normpath = os.path.normpath
    join = os.path.join
    return (lambda *base: normpath(join(dir, *base)).replace('\\', '/'))


def urljoin(base, *urls):
    """Modified from http://teethgrinder.co.uk/blog/Normalize-URL-path-python/
    >>> f = urljoin
    >>> f('http://site.com/', '/path/../path/.././path/./')
    'http://site.com/path'
    >>> f('http://site.com/path/x.html', '/path/../path/.././path/./y.html')
    'http://site.com/path/y.html'
    >>> f('http://site.com/', '../../../../path/')
    'http://site.com/path'
    >>> f('http://site.com/x/x.html', '../../../../path/moo.html')
    'http://site.com/path/moo.html'
    >>> f('http://site.com/99/x.html', '1/2/3/moo.html')
    'http://site.com/99/1/2/3/moo.html'
    >>> f('http://site.com/99/x.html', '../1/2/3/moo.html')
    'http://site.com/1/2/3/moo.html'
    >>> f('http://site.com/', 'a', 'b', 'c')
    'http://site.com/a/b/c'
    >>> f('http://site.com/', '..', '..', '..')
    'http://site.com/'
    >>> f('http://site.com/')
    'http://site.com/'
    """
    join = urlparse.urljoin(base, '/'.join(urls))
    url = list(urlparse.urlparse(join))
    url[2] = posixpath.normpath(url[2])
    return urlparse.ParseResult(*url).geturl()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
