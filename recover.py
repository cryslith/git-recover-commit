#!/usr/bin/env python3


import argparse
import sys
import os

from dulwich.client import get_transport_and_path
from dulwich.porcelain import default_bytes_err_stream


# adapted from dulwich.porcelain.push
def create_remote(remote_location, refs_to_create,
                  errstream=default_bytes_err_stream, **kwargs):
    """Remote creation of refs.
    Fails if remote ref already exists.
    Fails if remote does not have referenced commits

    :param remote_location: Location of the remote
    :param refs_to_create: map from ref name -> commit hash
    :param errstream: A stream file to write errors
    """

    client, path = get_transport_and_path(
            remote_location, **kwargs)

    def update_refs(refs):
        for (r, commit) in refs_to_create.items():
            if r in refs:
                raise Exception('Refusing to push ref {}: ref already exists on remote'.format(r))
            if not r.startswith(b'refs/heads/'):
                raise ValueError('Ref {} does not start with refs/heads/'.format(r))
        return refs_to_create

    def generate_pack_data(have, want, **kwargs):
        # Intentionally ignore whether the server says it has the refs
        # we want - we assume the server actually has everything
        # already
        return (0, ())

    client.send_pack(
        path, update_refs,
        generate_pack_data=generate_pack_data,
        progress=errstream.write)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('remote', help='url')
    parser.add_argument('branch', type=os.fsencode,
                        help='remote branch name to create')
    parser.add_argument('commit', type=os.fsencode,
                        help='full hash of commit for new branch to point to')
    args = parser.parse_args()

    create_remote(args.remote,
                  {b'refs/heads/' + args.branch:
                       args.commit})
    print('success', file=sys.stderr)

if __name__ == '__main__':
    main()
