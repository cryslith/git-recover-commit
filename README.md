# recover.py

A script to help with recovering an orphaned commit from a remote.

For instance, you force-push your branch away from the commit it was on.
You know what the full commit hash was,
but you don't have a local copy of the commit.
However, the commit is still there on the remote
because it hasn't been garbage-collected yet.
Unfortunately you can't just run `git fetch <commit>`
because it's not an advertised ref.

This script allows you to create a temporary branch on the remote server
pointing at the desired commit,
even though you don't have a copy of the commit in question.

## Usage

    recover.py git@example.com:repo.git temp-recovery-branch 0123456789012345678901234567890123456789

## Dependencies

- dulwich

## Alternatives

- If the remote has certain [configuration options][upconf] set,
  you may be able to just perform `git fetch <commit>`.
  Some remotes may have these set by default.
- If you're using GitHub, you can [use the GitHub API][ghapi]
  to do the same thing as this script.

[upconf]: https://stackoverflow.com/a/30701724/365902
[ghapi]: https://objectpartners.com/2014/02/11/recovering-a-commit-from-githubs-reflog/
