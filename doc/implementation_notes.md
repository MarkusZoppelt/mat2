Implementation notes
====================

Symlink attacks
---------------

MAT2 output predictable filenames (like yourfile.jpg.cleaned).
This may lead to symlink attack. Please check if you OS prevent
against them

Archives handling
-----------------

MAT2 doesn't support archives yet, because we haven't found an usable way to ask the user
what to do when a non-supported files are encountered.

PDF handling
------------

MAT was doing some kind of rendering for PDF files, on a cairo surface, then
printed it to a file. This kept the text selectable, but unfortunately, it
didn't remove any *deep metadata*, like the ones in embedded pictures. This was
on of the reason MAT was abandoned: the absence of satisfying solution to
handle PDF. But apparently, people are ok with [pdf redact
tools](https://github.com/firstlookmedia/pdf-redact-tools), that simply
transform the PDF into images. So this is what's MAT2 is doing too.

Images handling
---------------

When possible, images are handled like PDF: rendered on a surface, then saved
to the filesystem. This ensures that every metadata is removed.
