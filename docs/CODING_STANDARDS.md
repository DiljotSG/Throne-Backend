# Coding Standards

Our coding standards are almost entirely equivalent to pep8, which can be
found here:

https://www.python.org/dev/peps/pep-0008/

The only real difference is that we have a maximum line length of 127,
instead of 79, which we find needlessly restrictive.

In addition, we follow the philosophy that all of our code should be
self-documenting: Comments are only to be used when necessary, not peppered
in wherever.

These coding standards are enforced largely by flake8, which runs a check
after every pushed commit and disallows merging unless it passes.
