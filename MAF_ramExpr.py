#!/usr/bin/env python3

import random
import numpy, scipy.stats
import math
import datetime

FW_SIZE = 10
situation=3
FW = []



#application é a tupla (epsilon, probability, app_id)
application1=(5.0, 0.99, 'O')#OPLM
application2=(10.0, 0.99, 'B')#BM



def populate_FW():

	FW=[]
	for iterator in range(0,round(FW_SIZE/2)):
		if(situation==1):

			FW.append(numpy.random.normal(50,4))
			FW.append(numpy.random.normal(92,18))
		elif(situation==2):

			FW.append(numpy.random.normal(85,2))
			FW.append(numpy.random.normal(92,18))
		elif(situation==3):

			FW.append(numpy.random.normal(50,4))
			FW.append(numpy.random.normal(155,2))
		elif(situation==4):

			FW.append(numpy.random.normal(85,2))
			FW.append(numpy.random.normal(155,2))


	return FW	

def mean_confidence_interval(data, confidence):
	a = 1.0 * numpy.array(data)
	n = len(a)
	m, se = numpy.mean(a), scipy.stats.sem(a)
	h = se * scipy.stats.t.ppf((1+ confidence) / 2., n-1)

	return m, m-h, m+h

def range_interval(lower_bound=0.0, upper_bound=0.0):
	return upper_bound - lower_bound

def standardDeviationDoVector(dataset):
	media_local=0.0
	media_local=numpy.mean(dataset)
	soma=0
	if(len(dataset) == 1):
		return 0.0   
	else:
		for i in range(0, len(dataset)):
			soma=(soma + ( (dataset[i] - media_local) * (dataset[i] - media_local) ) )
		variance=(soma/( len(dataset) - 1.0) )
		return math.sqrt(variance)

def percentilDoVector(vector, percentil):
	index=(len(vector) * (percentil / 100.0))
	return vector[int(index)]

def skewnessDoVector(dataset):
	media_local=numpy.mean(dataset)
	p50=percentilDoVector(dataset, 50)
	sd=standardDeviationDoVector(dataset)
	CTE3=3.0
	cima=(media_local - p50)
	if(cima == 0.0):
		return 0.0
	return CTE3 * (cima/sd)

def DQAM(tau_epislon=0.0, tau_p=0.0, DI_RD=[], DI_pflag=0):
	intconf = mean_confidence_interval(DI_RD, tau_p)
	if ( range_interval(lower_bound=intconf[1], upper_bound=intconf[2]) <= 2 * tau_epislon ):

		qflag=1
		output_id=100
		return output_id, DI_RD, qflag
	else:
		if ( DI_pflag == 0):

			output_id=101
			return output_id, DI_RD
		else:

			qflag=0
			output_id=102
			return output_id, DI_RD, qflag 	
	

def DQEM(DI_RD=[]):
	me = numpy.mean(DI_RD)
	sk = skewnessDoVector(DI_RD)
	LD=[]
	HD=[]
	if( abs(sk) <= 1 ):

		pflag=1
		output_id=200
		return output_id, DI_RD, pflag
	else:
		for datapoint in DI_RD:

			if (datapoint <= me):
				LD.append(datapoint)
			else:
				HD.append(datapoint)
		pflag=0
		output_id=201
		return output_id, LD, HD, pflag 


def evaluate_dqam_result(DQAM_RESULT):
	if (DQAM_RESULT[0] == 100):

		sendToAppOrDqem = 'A'
		DI_RD=DQAM_RESULT[1]
		qflag=DQAM_RESULT[2]
		return sendToAppOrDqem, DI_RD, qflag
	elif (DQAM_RESULT[0] == 101):

		sendToAppOrDqem = 'D'
		DI_RD=DQAM_RESULT[1]
		return sendToAppOrDqem, DI_RD

		
	elif (DQAM_RESULT[0] == 102):

		print(DQAM_RESULT)
		sendToAppOrDqem = 'A'
		DI_RD=DQAM_RESULT[1]
		qflag=DQAM_RESULT[2]
		return sendToAppOrDqem, DI_RD, qflag


def Volcanus_main(FW, application):
	DQAM_RESULT = DQAM(tau_epislon=application[0], tau_p=application[1], DI_RD=FW, DI_pflag=0)
	
	dqam_result_evaluation = evaluate_dqam_result(DQAM_RESULT)


	if(dqam_result_evaluation[0] == 'A'):

		return dqam_result_evaluation[1], dqam_result_evaluation[2]	
	elif(dqam_result_evaluation[0] == 'D'):
		DQEM_RESULT = DQEM(dqam_result_evaluation[1])
		if (DQEM_RESULT[0] == 200):

			return DQEM_RESULT[1], 0
		elif (DQEM_RESULT[0] == 201):
			DQAM_RESULT_LD=DQAM(tau_epislon=application[0], tau_p=application[1], DI_RD=DQEM_RESULT[1], DI_pflag=0)
			DQAM_RESULT_HD=DQAM(tau_epislon=application[0], tau_p=application[1], DI_RD=DQEM_RESULT[2], DI_pflag=0)
            
			dqam_result_evaluation_LD = evaluate_dqam_result(DQAM_RESULT_LD)
			dqam_result_evaluation_HD = evaluate_dqam_result(DQAM_RESULT_HD)
			
			LD_toReturn=[]
			LD_quality=99			
			HD_toReturn=[]
			HD_quality=99
            
			if(dqam_result_evaluation_LD[0] == 'A'):

				LD_toReturn=dqam_result_evaluation_LD[1]
				LD_quality=dqam_result_evaluation_LD[2]
			elif(dqam_result_evaluation_LD[0] == 'D'):

				LD_toReturn=dqam_result_evaluation_LD[1]
				LD_quality=0

            
			if(dqam_result_evaluation_HD[0] == 'A'):

				HD_toReturn=dqam_result_evaluation_HD[1]
				HD_quality=dqam_result_evaluation_HD[2]

			elif(dqam_result_evaluation_HD[0] == 'D'):

				HD_toReturn=dqam_result_evaluation_HD[1]
				HD_quality=0
				
			
			return LD_toReturn, LD_quality, HD_toReturn, HD_quality

def MAF(datareceived):
	return numpy.mean(datareceived)
    
	
def applicationEvaluation(volcanus_result, application):
	

	
	if(application[2]=='O'): 
		if(numpy.random.randint(2)==1):
			healty=1
		else:
			healty=-1

		if(len(volcanus_result)==2): 
			media = MAF(volcanus_result[0])
			if(volcanus_result[1]==1): 
				if((media) > 40 and (media < 90) ):
					if(media > 65):
						#print("e0")
						healty=-1
					else:
						healty=1
				
		elif(len(volcanus_result)==4):
			
			media1 = MAF(volcanus_result[0])
			qflag1 = volcanus_result[1]
			media2 = MAF(volcanus_result[2])
			qflag2 = volcanus_result[3]
			
			if(qflag1==1):

				if((media1) > 40 and (media1 < 90) ):
					if(media1 > 65):
						healty=-1
					else:
						healty=1			
			if(qflag2==1 and healty==1):

				if((media1) > 40 and (media1 < 90) ):
					if(media1 > 65):
						healty=-1
					else:
						healty=1

		return healty
	
	elif(application[2]=='B'): 
		if(numpy.random.randint(2)==1):
			healty=1
		else:
			healty=-1

		if(len(volcanus_result)==2): 
			media = MAF(volcanus_result[0])
			if(volcanus_result[1]==1):
				if(media > 144):
					healty = -1;
				else:
					healty=1

		elif(len(volcanus_result)==4):

			media1 = MAF(volcanus_result[0])
			qflag1 = volcanus_result[1]
			media2 = MAF(volcanus_result[2])
			qflag2 = volcanus_result[3]
			
			if(qflag1==1):
				if(media1 > 144 ):
					healty=-1
				else:
					healty=1			
			if(qflag2==1 and healty==1):
				if(media2 > 144 ):
					healty=-1
				else:
					healty=1
		return healty




 







	
rodada = 1
while rodada < 30000:
	
	FW=populate_FW()
	
	FW.sort()
	
		

	print(applicationEvaluation((FW,1), application1))
	print(applicationEvaluation((FW,1), application2))

		
		
	rodada=rodada+1






	
