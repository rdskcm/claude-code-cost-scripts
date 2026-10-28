"""Where the transcripts come from; shared by every script.

Usage: python3 SCRIPT.py [DIR ...]

Each DIR is one project transcript directory, the kind Claude Code keeps at
~/.claude/projects/<project>/ (it holds <session>.jsonl files and
<session>/subagents/*.jsonl). Without DIR arguments the directories are taken
from $CLAUDE_TRANSCRIPTS_DIR (several joined with ':'); without that, every
project directory under ~/.claude/projects/ is read.
"""
import glob
import os
import sys

ENV = "CLAUDE_TRANSCRIPTS_DIR"
DEFAULT_ROOT = "~/.claude/projects"


def transcript_dirs():
    if sys.argv[1:2] in (["-h"], ["--help"]):
        print(__doc__)
        sys.exit(0)
    if len(sys.argv) > 1:
        dirs = sys.argv[1:]
    elif os.environ.get(ENV):
        dirs = [d for d in os.environ[ENV].split(os.pathsep) if d]
    else:
        root = os.path.expanduser(DEFAULT_ROOT)
        if not os.path.isdir(root):
            sys.exit(f"{root} does not exist; pass DIR arguments or set {ENV}")
        dirs = sorted(os.path.join(root, n) for n in os.listdir(root)
                      if os.path.isdir(os.path.join(root, n)))
    dirs = [os.path.abspath(os.path.expanduser(d)) for d in dirs]
    bad = [d for d in dirs if not os.path.isdir(d)]
    if bad:
        sys.exit("not a directory: " + ", ".join(bad))
    return dirs


def transcript_files():
    """(project_dir, path) for every .jsonl, directory by directory, glob order kept."""
    pairs = [(d, f) for d in transcript_dirs()
             for f in glob.glob(os.path.join(d, "**", "*.jsonl"), recursive=True)]
    if not pairs:
        sys.exit("no .jsonl transcripts found")
    return pairs
