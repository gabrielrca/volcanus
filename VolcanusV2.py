#!/usr/bin/env python3

import random
import numpy, scipy.stats
import math

FW_SIZE = 200
FW = []

#application é a tupla (epsilon, probability)
application1=(3.0, 0.99)
application2=(1000.0, 0.95)


def populate_FW():

	FW=[]
	situation=1
	#Falta implementar ainda montar o FW com os valores das situacoes
	for iterator in range(0,round(FW_SIZE/2)):
		if(situation==1):
			#sampleToReturn =  (generateSample.nextGaussian()* 4 ) + 50;
			#sampleToReturn =  (generateSample.nextGaussian()* 18) + 92;
			FW.append(numpy.random.normal(50,4))
			FW.append(numpy.random.normal(92,18))
		elif(situation==2):
			#sampleToReturn =   (generateSample.nextGaussian()* 2 ) + 85;
			#sampleToReturn =   (generateSample.nextGaussian()* 18) + 92;
			FW.append(numpy.random.normal(85,2))
			FW.append(numpy.random.normal(92,18))
		elif(situation==3):
			#sampleToReturn =  (generateSample.nextGaussian()* 4 ) + 50;
			#sampleToReturn =  (generateSample.nextGaussian()* 2) + 155;
			FW.append(numpy.random.normal(50,4))
			FW.append(numpy.random.normal(155,2))
		elif(situation==4):
			#sampleToReturn =  (generateSample.nextGaussian()* 2 ) + 85; 
			#sampleToReturn =  (generateSample.nextGaussian()* 2) + 155; 
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
		#The data meets the dq requirements of the application
		#print("(DI.RD, QFLAG = 1)")
		qflag=1
		output_id=100
		return output_id, DI_RD, qflag
	else:
		if ( DI_pflag == 0):
			#The data doesnt meet the dq requirements of the application, but hasnt been processed by DQEM
			#print(DQEM(DI_RD))
			output_id=101
			return output_id, DI_RD
		else:
			#The data doesnt meet the dq requirements of the application, and has been processed by DQEM
			#print("(DI.RD, QFLAG = 0)")
			qflag=0
			output_id=102
			return output_id, DI_RD, qflag 	
	

def DQEM(DI_RD=[]):
	me = numpy.mean(DI_RD)
	sk = skewnessDoVector(DI_RD)
	LD=[]
	HD=[]
	if( abs(sk) <= 1 ):
		#The data has to be sent to DQAM, but, DQEM did nothing
		pflag=1
		output_id=200
		return output_id, DI_RD, pflag
	else:
		for datapoint in DI_RD:
			#DQAM has broken the data and the greater and lower data has to be sent to DQAM to be re evaluated
			if (datapoint <= me):
				LD.append(datapoint)
			else:
				HD.append(datapoint)
		pflag=0
		output_id=201
		return output_id, LD, HD, pflag 


def evaluate_dqam_result(DQAM_RESULT):
	if (DQAM_RESULT[0] == 100):
		#The data meets the dq requirements of the application
		#should be sent to the app
		#print(DQAM_RESULT)
		sendToAppOrDqem = 'A'
		DI_RD=DQAM_RESULT[1]
		qflag=DQAM_RESULT[2]
		return sendToAppOrDqem, DI_RD, qflag
	elif (DQAM_RESULT[0] == 101):
		#The data doesnt meet the dq requirements of the application, but hasnt been processed by DQEM
		sendToAppOrDqem = 'D'
		DI_RD=DQAM_RESULT[1]
		return sendToAppOrDqem, DI_RD

		
	elif (DQAM_RESULT[0] == 102):
		#The data doesnt meet the dq requirements of the application, and has been processed by DQEM
		#should be sent to the app
		print(DQAM_RESULT)
		sendToAppOrDqem = 'A'
		DI_RD=DQAM_RESULT[1]
		qflag=DQAM_RESULT[2]
		return sendToAppOrDqem, DI_RD, qflag


def Volcanus_main(FW, application):
	DQAM_RESULT = DQAM(tau_epislon=application[0], tau_p=application[1], DI_RD=FW, DI_pflag=0)
	
	dqam_result_evaluation = evaluate_dqam_result(DQAM_RESULT)


	if(dqam_result_evaluation[0] == 'A'):
		#aqui devo enviar direto para aplicacao
		print("1)Enviar para app com qualidade: " + str(dqam_result_evaluation[2]))
		return dqam_result_evaluation[1], dqam_result_evaluation[2]	
	elif(dqam_result_evaluation[0] == 'D'):
		DQEM_RESULT = DQEM(dqam_result_evaluation[1])
		if (DQEM_RESULT[0] == 200):
			print("2)Enviar para app com qualidade: 0 ")
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
                #aqui devo enviar direto para aplicacao
				print("3)Enviar para app com qualidade: " + str(dqam_result_evaluation_LD[2]))
				LD_toReturn=dqam_result_evaluation_LD[1]
				LD_quality=dqam_result_evaluation_LD[2]
			elif(dqam_result_evaluation_LD[0] == 'D'):
                #aqui devo enviar direto para aplicacao, e devo lembrar que devo colocar o qflag como 0.. ou seja ele quebrou mas msm assim n conseguiu
				print("4)Enviar para app com qualidade: 0 ")
				LD_toReturn=dqam_result_evaluation_LD[1]
				LD_quality=0

            
			if(dqam_result_evaluation_HD[0] == 'A'):
                #aqui devo enviar direto para aplicacao
				print("5)Enviar para app com qualidade: " + str(dqam_result_evaluation_LD[2]))
				HD_toReturn=dqam_result_evaluation_LD[1]
				HD_quality=dqam_result_evaluation_LD[2]

			elif(dqam_result_evaluation_HD[0] == 'D'):
                #aqui devo enviar direto para aplicacao, e devo lembrar que devo colocar o qflag como 0.. ou seja ele quebrou mas msm assim n conseguiu
				print("6)Enviar para app com qualidade: 0 ")
				HD_toReturn=dqam_result_evaluation_LD[1]
				HD_quality=0
			
			return LD_toReturn, LD_quality, HD_toReturn, HD_quality

            
	
		


while True:
	
	FW=populate_FW()

	print("app1")
	print(Volcanus_main(FW, application1))
	print("app2")
	print(Volcanus_main(FW, application2))
	
	
