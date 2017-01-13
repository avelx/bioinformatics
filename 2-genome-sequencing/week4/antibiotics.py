import sys
sys.path.insert(0,'../')
from common import RNA_codon_table, Integer_mass_table, aminoacids_tbl, PeptidesMasses, PeptideMass
sys.path.insert(0,'../week3')
from protein import SubpeptidesCyclic, SubpeptidesNotCyclic
import timeit

def CyclopeptideScoring(peptide,spectrum,Cyclic,im_tbl):
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
    
  #print '{} has score {} for spectrum'.format(peptide,score)
  return score
  
def LeaderBoardExpand(LeaderBoard,aminos):
  expand = []
  for peptide in LeaderBoard:
    for a in aminos :
      expand.append(peptide+a)
  return expand

def LeaderBoardTrim(scored_LeaderBoard, N):  
  if len(scored_LeaderBoard) <= N:
    return scored_LeaderBoard    
  # sort LeaderBoard according to the decreasing order of scores in LinearScores
  scored_LeaderBoard = sorted(scored_LeaderBoard, key=lambda x: x[1], reverse=True) 
  # return top N peptides       
  Nth_score = scored_LeaderBoard[N-1][1] # score
  # allow ties 
  scored_LeaderBoard = [x for x in scored_LeaderBoard if x[1] >= Nth_score]  
  return scored_LeaderBoard
  
def LeaderBoardCyclopeptideSequencing(spectrum,N, Cyclic, aminos_tbl,im_tbl):  
  aminos = aminos_tbl.keys()
    
  spectrum = sorted(spectrum)    
  LeaderScore = CyclopeptideScoring('', spectrum, Cyclic,im_tbl)
  LeaderPeptides = []
    
  LeaderBoard = [('', LeaderScore, 0)]
  ParentMass = spectrum[-1]  
    
  while len(LeaderBoard)>0:       
    # expand LeaderBoard
    LeaderBoard = [(
      peptide, 
      CyclopeptideScoring(peptide, spectrum, False,im_tbl), # linear scoring for trimming
      PeptideMass(peptide,im_tbl), # mass       
      CyclopeptideScoring(peptide, spectrum, Cyclic,im_tbl), # <cyclic?> score is only used for comparing with the leader peptide(s).
    ) for peptide in LeaderBoardExpand([x[0] for x in LeaderBoard],aminos)]
  
    # If if Mass(Peptide) = ParentMass(Spectrum) and Score(Peptide, Spectrum) > Score(LeaderPeptide, Spectrum) then update LeaderPeptide        
    for (peptide,score) in [(x[0],x[3]) for x in LeaderBoard if x[2] == ParentMass and x[3] >= LeaderScore]:      
      if score > LeaderScore:    
        LeaderScore = score
        LeaderPeptides = []
        LeaderPeptides.append(peptide)
      elif score == LeaderScore:
        LeaderPeptides.append(peptide)      
           
    # remove Peptide from LeaderBoard if Mass(Peptide) > ParentMass(Spectrum)                        
    LeaderBoard = [x for x in LeaderBoard if x[2] <= ParentMass]
    
    # Trim LeaderBoard w.r.t. N        
    LeaderBoard = LeaderBoardTrim(LeaderBoard, N)

  print 'Total of {} leader peptides with score {}'.format(len(LeaderPeptides), LeaderScore)  
  return ['-'.join([str(aminos_tbl[a][2]) for a in peptide]) for peptide in LeaderPeptides]  
  
def main_CyclopeptideScoringProblem(myfile,Cyclic):
  inputFile = myfile + '.txt'
  outputFile = myfile + '.out'
  with open(inputFile) as inFile:
    peptide = inFile.readline().strip()
    spectrum = [int(x) for x in inFile.readline().strip().split(' ')]
  
  score = CyclopeptideScoring(peptide, spectrum, Cyclic)  
  with open(outputFile,'w') as outFile:    
    outFile.write(str(score))
  
def main_LeaderBoardCyclopeptideSequencing(myfile,Cyclic,print_all,synthetic_aminos=False):
  inputFile = myfile + '.txt'
  outputFile = myfile + '.out'
  start = timeit.default_timer()
  
  with open(inputFile) as inFile:
    N = int(inFile.readline().strip())
    spectrum = [int(x) for x in inFile.readline().strip().split(' ')]
   
  if synthetic_aminos: 
    aminos_tbl={}
    im_tbl={}
    for da in range(57,201):      
      aminos_tbl[chr(da)]=(chr(da),chr(da),da)
      im_tbl[chr(da)]=da
  else :
    im_tbl = Integer_mass_table()  
    aminos, aminos_tbl = aminoacids_tbl(im_tbl,True)
  
  leader_peptides = LeaderBoardCyclopeptideSequencing(spectrum,N,Cyclic,aminos_tbl,im_tbl)
  
  with open(outputFile,'w') as outFile:
    if print_all:
      txt = ' '.join(leader_peptides)
    else:
      txt = leader_peptides[0]
    outFile.write(txt)    
  
  stop = timeit.default_timer()
  print 'Running time {} sec'.format(stop - start)
 
def main_Trim(myfile):
  inputFile = myfile + '.txt'
  outputFile = myfile + '.out'
  start = timeit.default_timer()
  
  with open(inputFile) as inFile:
    LeaderBoard = [x for x in inFile.readline().strip().split(' ')]
    spectrum = [int(x) for x in inFile.readline().strip().split(' ')]
    N = int(inFile.readline().strip())
  
  scored_LeaderBoard = [(
    peptide,
    CyclopeptideScoring(peptide, spectrum, False), # score    
  ) for peptide in LeaderBoard]  
  trimmed = LeaderBoardTrim(scored_LeaderBoard, N)  
  
  with open(outputFile,'w') as outFile:    
    txt=' '.join([x[0] for x in trimmed])
    outFile.write(txt)
    print txt
  
'''
main_CyclopeptideScoringProblem('sample_cyclopeptidescoring',True) #11
main_CyclopeptideScoringProblem('cyclopeptide_scoring',True) #521
main_CyclopeptideScoringProblem('dataset_102_3',True)
main_CyclopeptideScoringProblem('linear_score',False) #8
main_CyclopeptideScoringProblem('dataset_4913_1',False) #8
main_Trim('sample_trim')
main_Trim('dataset_4913_3')
'''
#main_LeaderBoardCyclopeptideSequencing('sample_linearpeptidescoring',False,False)
#main_LeaderBoardCyclopeptideSequencing('dataset_102_8',False,False)
#main_LeaderBoardCyclopeptideSequencing('dataset_102_10',True,True)
main_LeaderBoardCyclopeptideSequencing('dataset_103_2',True,True,True)