# Clean shared now state

Both set_now and take_photo validate the original location and activity before
storing shared state. URLs, mentions and long numbers are rejected; known names
are removed, and empty or longer than 12 characters are rejected. The source
place is recorded for later use and is not shown in the shared now line.

The existing phone switches still apply. No plugin methods or other files were
changed. Full-suite testing was not requested; targeted test results are reported
with the change.
