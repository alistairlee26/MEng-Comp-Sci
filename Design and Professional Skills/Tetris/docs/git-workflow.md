# Publishing player changes

This workspace keeps the original game files tracked and publishes changes to
`player.py`. Development scripts, tests, reports, documentation and editor settings
remain on disk and are ignored by Git.

Use these commands for subsequent player updates:

```powershell
git add -- player.py
git commit -m "Improve player"
git push
```

Local hooks in `.git/hooks/pre-commit` and `.git/hooks/pre-push` reject changes
outside `player.py`. The push hook checks each outgoing commit, including changes
that were added and later removed. It allows the prepared cleanup commit as a
one-time exception. These hooks protect this checkout and are not installed
automatically on another computer or in a fresh clone.

If another tracked file is accidentally staged, unstage it while keeping the local
edit:

```powershell
git restore --staged -- path/to/file
```

The cleanup commit is `637604070d83eed1b9fcf044e792599cca8bb7c0`. It removes 78
supporting files from the repository tree while retaining all their local copies.
It does not change `player.py`. The preceding accidental commit remains in Git
history; the cleanup does not rewrite or erase that history.

Pushing the cleanup can queue another grader run. It was pushed after explicit
confirmation that any new grader run would be cancelled by the user.
