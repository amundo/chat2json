from glob import glob
import os
import chat
import json

childes_dir = '/Users/pat/Sites/ucsb/courses/2011/lgacq/childes/Eng-USA/'
corpora = glob(childes_dir + '*')

childes = {}

for c in corpora:
  if  os.path.isdir(c):
    childes[c] = glob(c + '/*')

#for a,b in [(k.split('/')[-1], len(v)) for k,v in childes.items()]: print b,a

def process_corpus(corpus):
  transcripts = {}
  for filename in corpus:
    transcripts[filename] = open(filename).read().decode('utf-8')

 
if __name__ == "__main__":
  pass # ('/Users/pat/Sites/ucsb/courses/2011/lgacq/childes/Eng-USA/MacWhinney/54a1.cha')
