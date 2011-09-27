#!/usr/bin/env python
import json
"""
parse_chat.py - Convert a .chat transcript into JSON


"""

sample = u"""@Begin
@Languages:	eng
@Participants:	CHI Adam Target_Child, MOT Mother, FAT Father, URS Ursula_Bellugi Investigator, RIC Richard_Cromer Investigator
@ID:	eng|brown|CHI|2;7.01|male|normal|middle_class|Target_Child||
@ID:	eng|brown|MOT|||||Mother||
@ID:	eng|brown|FAT|||||Father||
@ID:	eng|brown|URS|||||Investigator||
@ID:	eng|brown|RIC|||||Investigator||
@Date:	04-FEB-1963
@Time Duration:	10:20-11:20
*CHI:	dat [: that] a handle [?] .
%mor:	pro:dem|that det|a n|handle .
%gra:	1|3|SUBJ 2|3|DET 3|0|ROOT 4|3|PUNCT
*CHI:	hand me piece a paper .
%mor:	v|hand pro|me v|piece det|a n|paper .
%gra:	1|0|ROOT 2|1|OBJ 3|1|COMP 4|5|DET 5|3|OBJ 6|1|PUNCT
%add:	Ursula
*URS:	alright .
%mor:	co|alright .
%gra:	1|0|ROOT 2|1|PUNCT
*MOT:	please .
%mor:	co|please .
%gra:	1|0|ROOT 2|1|PUNCT
*CHI:	please .
%mor:	co|please .
%gra:	1|0|ROOT 2|1|PUNCT
%spa:	$IMIT
@End
"""

def read_transcript(filename):
  return open(filename, 'U').read().decode('utf-8')
  
def get_line(pattern, content):
  lines = content.splitlines()
  return [line for line in lines if line.startswith(pattern)]
   
def get_languages(content):
  return get_line('@Languages:', content)

def get_id(content):
  return get_line('@ID:', content)

def get_date(content):
  return get_line('@Date:', content)

def get_time_duration(content):
  return get_line('@Time Duration:', content)

def squish_continuation_lines(content):
  """
  most lines in a chat transcript look like:
  
%gra:	1|2|SUBJ 2|0|ROOT 3|2|PRED 4|3|XMOD 5|4|OBJ 6|2|PUNCT

  but some span more than one line:  

*MOT:	he's started being very particular about saying two this or two
	that .

  Make the second case look like the first.
  """
  sigils = '@%*'
  lines = content.splitlines()
  fixed = [lines[0]] 
  for line in lines[1:]:
    if line[0] not in sigils: 
      fixed[-1] += ' ' + line.strip() 
    else:  
      fixed.append(line.strip())
  return '\n'.join(fixed)

def parse_turns(content):
  pass

def parse_transcript(content):
  transcript = {}
  content = squish_continuation_lines(content)
  transcript['languages'] = get_languages(content)
  transcript['id'] = get_id(content)
  transcript['date'] = get_date(content)
  transcript['time_duration'] = get_time_duration(content)
  #transcript['content'] = parse_turns(content)

  return transcript

if __name__ == "__main__":
  import sys
  filename = sys.argv[1]
  content = open(filename, 'U').read().decode('utf-8')
  print json.dumps(parse_transcript(content), indent=2)

