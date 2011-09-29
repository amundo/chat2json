#!/usr/bin/env python
import json
import re
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

def remove_spaces_and_sigils(label):
  sigils = '@%*'
  for sigil in sigils:
    label = label.replace(sigil, '')
  return label.lower().replace(' ', '_')

def get_attribute(line):
  try: 
    attribute, content = line.split(':', 1)
    return remove_spaces_and_sigils(attribute).strip(), content.strip()
  except ValueError:
    print 'ERROR Unable to parse attribute line: ', 
    print line
    exit()

def parse_participants(participant_line):
  """
  CHI Adam Target_Child, MOT Mother, FAT Father, URS Ursula_Bellugi Investigator, RIC Richard_Cromer Investigator

  parse this to produce:
  { 
    'CHI' : 'Adam Target_Child',
    'MOT' : 'Mother',
    'FAT' : 'Father',
    'URS' : 'Ursula_Bellugi Investigator',
    'RIC' : 'Richard_Cromer Investigator'
  } 
  """
  participants = {} 
  abbreviation_and_name = [element.split() for element in line.split(',')]
  for abbreviation, name in abbreviation_and_name:
    participants[abbreviation] = name
  return participants

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

def chunk_list(sequence, criterion):
  """
  Subdivide a sequence into subsequences based on a criterion
  """
  a = 0
  chunk = []

  result = []

  for element in sequence:
    if criterion(element):
      a = a + 1
    if a == 1:
      chunk.append(element)
    else:
      result.append(chunk)
      chunk = []
      chunk.append(element)
      a = 1
  result.append(chunk)
  return result

def starts_with_star(line):
  return line.startswith('*') 
 
def parse_transcript(content):
  """
  parse the content of the chat content into a JSON structure
  """
  transcript = {}
  transcript['turns']  = []
  transcript['lines']  = []

  content = squish_continuation_lines(content)

  for line in content.splitlines():
    if line.startswith('@') and ':' in line:
      attribute, value = get_attribute(line)
      transcript[attribute] = value
    else:
      transcript['lines'].append(line)

  transcript['turns'] = chunk_list(transcript['lines'], starts_with_star)
  ignore = transcript.pop('lines') 

  return transcript

if __name__ == "__main__":
  import sys
  filename = sys.argv[1]
  content = open(filename, 'U').read().decode('utf-8')
  print json.dumps(parse_transcript(content), indent=2)

