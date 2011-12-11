import sys, json, random
from collections import defaultdict
from textutil import *

def tokenize(text): return text.lower().split()

class Transcript:
  """
  should be subclassable - ChildesTranscript, etc
  """

  def __init__(self, filename):
    self.content = self.load_chat_file(filename)
    self.filename = filename
    self.turns = self.content['turns'] 
    self.speakers = self._collect_speakers()
    self.words = self.build_wordlist()
    self.dispersion_map = self.build_dispersion_map()

  def load_chat_file(self, filename):
    return json.load(open(filename))

  def build_wordlist(self):
    wordlist = []
    for turn in self.turns:
      turn_words = tokenize(turn['sentence'])
      wordlist.extend(turn_words)
    return wordlist

  def build_dispersion_map(self):
    dmap = defaultdict(list)
    for i, word in enumerate(self.words):
      dmap[word].append(i)
    return dmap 

  def dispersion(self, word):
    if word in self.dispersion_map: 
      return self.dispersion_map[word] 

  def _collect_speakers(self):
    return sorted(set([turn['speaker'] for turn in self.turns]))

  def words_by_speaker(self, speaker):
    if speaker not in self.speakers: 
      sys.stderr.write('speaker [%s] not in transcript' % speaker)
    else: 
      return tokenize(' '.join([(turn['sentence']) for turn in self.turns]))


class Archive:
  """
  collection of transcripts
  """
  def __init__(self,filenames):
    #print "filenames are: " + ' '.join(filenames)
    self.transcripts = []
    self.load_transcripts(filenames)

  def load_transcripts(self, filenames):
    """
    this should somehow validate that it's a CHAT json file
    """
    for filename in filenames: 
      #print filename
      try: 
        transcript = Transcript(filename)
        self.transcripts.append(transcript)
      except:
        sys.stderr.write('Problem loading file: %s\n' % filename) 

if __name__ == "__main__":
  #q = Transcript(sys.argv[5])
  #print q
  #print q.words_by_speaker('CHI'); exit()
  import sys
  archive = Archive(sys.argv[1:])
  #print archive.transcripts
  #transcript = random.choice(archive.transcripts)
  print archive.transcripts

  words = 'bird mommy naima the'.split()

  query = defaultdict()

  for transcript in archive.transcripts:
    query[transcript.filename] = {}
    for word in words: 
      query[transcript.filename][word] = len(transcript.dispersion(word))

  print json.dumps(query, indent=2)
  #print transcript.words_by_speaker('FAT')
  #print transcript.dispersion_map('bird')

