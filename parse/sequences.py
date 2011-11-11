#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
sequences.py - a utility for subdividing sequences based on
  criteria.

For instance; 


"""
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
