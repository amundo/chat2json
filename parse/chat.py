#!/usr/bin/env python
import json
import re
from sequences import * 
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
  return label.replace(' ', '_')

def get_attribute(line):
  try: 
    attribute, content = line.split(':', 1)
    attribute = remove_spaces_and_sigils(attribute).strip()
    content = content.strip()
    return attribute, content
  except ValueError:
    print 'ERROR Unable to parse attribute line: ', 

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


def starts_with_star(line):
  return line.startswith('*') 
 
def parse_analysis(gra, mor, sentence):
  """
  stitch together %gra, %mor, and sentence  
  """
  #print gra, '\n', mor, '\n', sentence
  gra = gra.strip().split(' ')
  mor = mor.strip().split(' ')
  words = sentence.strip().split()
  return zip(mor, gra, words) 


def parse_turn(lines):
  """
  convert before into turn.
  before = [
    "*CLN:\twatch it spin .", 
    "%mor:\tn|watch pro|it v|spin .", 
    "%gra:\t1|3|VOC 2|3|SUBJ 3|0|ROOT 4|3|PUNCT", 
    "%spa:\t$DJF:RP"
  ] 

  turn = {
    'speaker' : 'CLN',
    'start' : 1368280,
    'stop'  : 1368698,
    'phrase' : {
      'sentence': 'watch it spin .',
      'mor': 'n|watch pro|it v|spin .',
      'gra' : '1|3|VOC 2|3|SUBJ 3|0|ROOT 4|3|PUNCT', 
      'spa' : '$DJF:RP'
    },
    'gloss' : dict(zip('sentence'.split(), 'gra'.split()) )

  }
  """

  turn = {} 

  for line in lines: 
    if line.startswith('*'): 
      turn['speaker'] = remove_spaces_and_sigils(line.split(':')[0]) 
      sentence, start, stop = process_sentence(line) 
      turn.update({'sentence': sentence, 'start':start, 'stop':stop}) 
    elif line.startswith('%'): 
      label, content = line.split('\t')
      kind = label[1:4]
      turn[kind] = content

  #print json.dumps(turn['phrase'], indent=2)
  if 'gra' in turn and 'mor' in turn and 'sentence' in turn: 
    turn['analysis'] = parse_analysis( turn['gra'], turn['mor'], turn['sentence'] )

  return turn

def extract_timestamps(line):
    return line.strip().split()[-1].split('_')

def process_sentence(line):
  #if '\t'  in line: 
  #  print line.replace('\t', '*****')

  line = line.replace(u'\u0015', '') # not sure what these are?

  line = line.split('\t')[1].strip()

  if re.search('(\d+)_(\d+)', line):
    start, stop = extract_timestamps(line)
    sentence = ' '.join(line.split(' ')[:-1])
    #print start, stop, '\n', sentence; exit()
  else: 
    sentence = ' '.join(line.split(' ')[:-1])
    start, stop = '0 0'.split() # may as well treat them as strings
  return sentence, start, stop

def parse_transcript(cha):
  """
  parse the contents of a chat file into a JSON structure
  """
  transcript = {}
  transcript['turns']  = []
  transcript['lines']  = []
  transcript['metadata']  = {}
  transcript['metadata']['filename'] = cha

  content = open(cha,'U').read().decode('utf-8')
  content = squish_continuation_lines(content)

  for line in content.splitlines():
    if line.startswith('@') and ':' in line:
      attribute, value = get_attribute(line)
      transcript['metadata'][attribute] = value
    elif line.startswith('@'):
      continue
    else:
      transcript['lines'].append(line)

  transcript['turns'] = chunk_list(transcript['lines'], starts_with_star)
  transcript['turns']  = [parse_turn(turn) for turn in transcript['turns']]

  ignore = transcript.pop('lines') 

  return transcript


if __name__ == "__main__":
  from search import * 
  from random import * 
  content = parse_transcript( choice(glob('/Users/pat/Sites/ucsb/courses/2011/lgacq/childes/Eng-USA/MacWhinney/*.cha')) )
  print '-------'
  print json.dumps(content, indent=2)
  
