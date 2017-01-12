import sys
sys.path.insert(0,'../')
from common import RNA_codon_table, Integer_mass_table, aminoacids_tbl, PeptidesMasses, PeptideMass
sys.path.insert(0,'../week3')
from protein import SubpeptidesCyclic, SubpeptidesNotCyclic
import timeit

im_tbl = Integer_mass_table()  

def CyclopeptideScoring(peptide,spectrum,Cyclic):
  spectrum=spectrum[:]
  if Cyclic: 
    subpeptides = SubpeptidesCyclic(peptide)
  else :
    subpeptides = SubpeptidesNotCyclic(peptide)
 
  score=0
  for sub in subpeptides:
    mass = PeptideMass(sub,im_tbl)
    if mass in spectrum:      
      score+=1
      spectrum.remove(mass)
    
  print '{} has score {} for spectrum'.format(peptide,score)
  return score
  
def LeaderboardExpand(leaderboard,aminos):
  expand = []
  for peptide in leaderboard:
    for a in aminos :
      expand.append(peptide+a)
  return expand

def LeaderboardTrim(leaderboard, spectrum, N):  
  # Calcualte the LinearScores for Leaderboard
  score_tuple = [(peptide,CyclopeptideScoring(peptide, spectrum, False)) for peptide in leaderboard]  
  # sort Leaderboard according to the decreasing order of scores in LinearScores
  score_tuple = sorted(score_tuple, key=lambda x: x[1], reverse=True) 
  # return top N peptides
  trimmed = score_tuple[:N]  
  return [x[0] for x in trimmed]
  
def LeaderboardCyclopeptideSequencing(spectrum,N):  
  Cyclic=False
  leader_peptide = ''
  leaderboard = [leader_peptide]
  leader_score = CyclopeptideScoring(leader_peptide, spectrum, Cyclic)
  parentmass = spectrum[-1]  
  aminos, aminos_tbl = aminoacids_tbl(im_tbl,True)
  aminos = [a for a in aminos if aminos_tbl[a][2] in spectrum]
    
  while len(leaderboard)>0:    
    leaderboard = LeaderboardExpand(leaderboard,aminos)
    print len(leaderboard)
    for peptide in leaderboard:
      mass = PeptideMass(peptide,im_tbl)
      if mass == parentmass :
        score = CyclopeptideScoring(peptide, spectrum, Cyclic)
        if score > leader_score:
          leader_peptide = peptide
          leader_score = score
          print 'leader',peptide
      elif mass > parentmass :
        leaderboard.remove(peptide)        
    leaderboard = LeaderboardTrim(leaderboard,spectrum,N)
  return [aminos_tbl[a][2] for a in leader_peptide]
  
def main_CyclopeptideScoringProblem(myfile,Cyclic):
  inputFile = myfile + '.txt'
  outputFile = myfile + '.out'
  with open(inputFile) as inFile:
    peptide = inFile.readline().strip()
    spectrum = [int(x) for x in inFile.readline().strip().split(' ')]
  
  score = CyclopeptideScoring(peptide, spectrum, Cyclic)  
  with open(outputFile,'w') as outFile:    
    outFile.write(str(score))
  
def main_LeaderboardCyclopeptideSequencing(myfile):
  inputFile = myfile + '.txt'
  outputFile = myfile + '.out'
  start = timeit.default_timer()
  
  with open(inputFile) as inFile:
    N = int(inFile.readline().strip())
    spectrum = [int(x) for x in inFile.readline().strip().split(' ')]
  
  leader_peptide = LeaderboardCyclopeptideSequencing(spectrum,N)
  
  with open(outputFile,'w') as outFile:    
    txt='-'.join([str(p) for p in leader_peptide])
    outFile.write(txt)
    print txt
  
  stop = timeit.default_timer()
  print 'Running time {} sec'.format(stop - start)
 
def main_Trim(myfile):
  inputFile = myfile + '.txt'
  outputFile = myfile + '.out'
  start = timeit.default_timer()
  
  with open(inputFile) as inFile:
    leaderboard = [x for x in inFile.readline().strip().split(' ')]
    spectrum = [int(x) for x in inFile.readline().strip().split(' ')]
    N = int(inFile.readline().strip())
    
  trimmed = LeaderboardTrim(leaderboard, spectrum, N)
  
  with open(outputFile,'w') as outFile:    
    txt=' '.join(trimmed)
    outFile.write(txt)
    print txt
  
'''
main_CyclopeptideScoringProblem('sample_cyclopeptidescoring',True) #11
main_CyclopeptideScoringProblem('cyclopeptide_scoring',True) #521
main_CyclopeptideScoringProblem('dataset_102_3',True)
main_CyclopeptideScoringProblem('linear_score',False) #8
main_CyclopeptideScoringProblem('dataset_4913_1',False) #8
'''
main_Trim('sample_trim')
main_Trim('dataset_4913_3')
#main_LeaderboardCyclopeptideSequencing('sample_linearpeptidescoring')
#main_LeaderboardCyclopeptideSequencing('dataset_102_8')


