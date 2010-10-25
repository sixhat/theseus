#!/usr/bin/env python
# encoding: utf-8
"""
dnet.py

a Telnet Library to Connect to Guess

Created by David Rodrigues on 2010-02-17.
Copyright (c) 2010 Sixhat Pirate Parts. All rights reserved.
"""

import sys
import os
import telnetlib
import time

class Dnet():
    """
    Constructor for a telnet library to connect to Guess
    See Guess - http://graphexploration.cond.org/
    """
    def __init__(self, gr):
        self.graph=gr
        if self.graph:
            self.tn=telnetlib.Telnet('localhost', 2222)

    def send(self, cmd):
        """
        Send a message to Guess via telnet.
        Guess - http://graphexploration.cond.org/
        """
        if self.graph:
            self.tn.write(cmd+"\n")
            self.tn.read_until("Done")
