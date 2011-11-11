#!/usr/bin/env python
import sys, os
from glob import glob
from random import choice
import json
import re
from sequences import * 
from chat import * 


def random_file():
  cha_file = choice(glob('/Users/pat/Sites/ucsb/courses/2011/lgacq/childes/Eng-USA/MacWhinney/*.json'))
  return json.load(open(cha_file))

if __name__ == "__main__":
  print json.dumps(random_file(), indent=2)

