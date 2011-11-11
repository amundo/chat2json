#!/usr/bin/env python
import sys, os
from glob import glob
from random import choice
import json
import re
from sequences import * 
from chat import * 

macwhinney = glob('/Users/pat/Sites/ucsb/courses/2011/lgacq/childes/Eng-USA/MacWhinney/*.cha')

for cha_file in macwhinney:
  new_json_file = cha_file.replace('.cha', '.json')
  open(new_json_file, 'w').write( json.dumps(parse_transcript(cha_file), indent=2) )



