from __future__ import absolute_import, unicode_literals

import os

import six
from raven.exceptions import InvalidGitRepository


def fetch_git_sha(path, head=None):
    """
    >>> fetch_git_sha(os.path.dirname(__file__))
    """
    if not head:
        head_path = os.path.join(path, '.git', 'HEAD')
        if not os.path.exists(head_path):
            raise InvalidGitRepository('Cannot identify HEAD for git repository at %s' % (path,))

        with open(head_path, 'r') as fp:
            head = six.text_type(fp.read()).strip()

        if head.startswith('ref: '):
            revision_file = os.path.join(
                path, '.git', *head.rsplit(' ', 1)[-1].split('/')
            )
        else:
            return head
    else:
        revision_file = os.path.join(path, '.git', 'refs', 'heads', head)

    if not os.path.exists(revision_file):
        if not os.path.exists(os.path.join(path, '.git')):
            raise InvalidGitRepository('%s does not seem to be the root of a git repository' % (path,))
        raise InvalidGitRepository('Unable to find ref to head "%s" in repository' % (head,))

    fh = open(revision_file, 'r')
    try:
        return six.text_type(fh.read()).strip()
    finally:
        fh.close()