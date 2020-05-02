#!/usr/bin/env python3

import random
import numpy, scipy.stats
import math
import datetime

FW_SIZE = 10
situation=3
FW = []
Run='V'

#statistics for evaluation
acertoBateria = 0.0
erroBateria =  0.0
acertoLinha =  0.0
erroLinha =  0.0

#VP VN FP FN da bateria
truePositive_bm =  0.0
trueNegative_bm =  0.0
falsePositive_bm =  0.0
falseNegative_bm =  0.0

#VP VN FP FN da linha
truePositive_oplm =  0.0
trueNegative_oplm =  0.0
falsePositive_oplm =  0.0
falseNegative_oplm =  0.0


#application é a tupla (epsilon, probability, app_id)
application1=(5.0, 0.99, 'O')#OPLM
application2=(10.0, 0.99, 'B')#BM



def populate_FW():

	FW=[]
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
		#print("1)Enviar para app com qualidade: " + str(dqam_result_evaluation[2]))
		return dqam_result_evaluation[1], dqam_result_evaluation[2]	
	elif(dqam_result_evaluation[0] == 'D'):
		DQEM_RESULT = DQEM(dqam_result_evaluation[1])
		if (DQEM_RESULT[0] == 200):
			#print("2)Enviar para app com qualidade: 0 ")
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
				#print("3)Enviar para app com qualidade: " + str(dqam_result_evaluation_LD[2]))
				LD_toReturn=dqam_result_evaluation_LD[1]
				LD_quality=dqam_result_evaluation_LD[2]
			elif(dqam_result_evaluation_LD[0] == 'D'):
                #aqui devo enviar direto para aplicacao, e devo lembrar que devo colocar o qflag como 0.. ou seja ele quebrou mas msm assim n conseguiu
				#print("4)Enviar para app com qualidade: 0 ")
				LD_toReturn=dqam_result_evaluation_LD[1]
				LD_quality=0

            
			if(dqam_result_evaluation_HD[0] == 'A'):
                #aqui devo enviar direto para aplicacao
				#print("5)Enviar para app com qualidade: " + str(dqam_result_evaluation_LD[2]))
				HD_toReturn=dqam_result_evaluation_HD[1]
				HD_quality=dqam_result_evaluation_HD[2]

			elif(dqam_result_evaluation_HD[0] == 'D'):
                #aqui devo enviar direto para aplicacao, e devo lembrar que devo colocar o qflag como 0.. ou seja ele quebrou mas msm assim n conseguiu
				#print("6)Enviar para app com qualidade: 0 ")
				HD_toReturn=dqam_result_evaluation_HD[1]
				HD_quality=0
				
			
			return LD_toReturn, LD_quality, HD_toReturn, HD_quality

def MAF(datareceived):
	return numpy.mean(datareceived)
    
	
def applicationEvaluation(volcanus_result, application):
	
	#print(volcanus_result[1])
	
	if(application[2]=='O'): #essa e a OPLM
		if(numpy.random.randint(2)==1):
			healty=1
		else:
			healty=-1

		if(len(volcanus_result)==2): #passar
			media = MAF(volcanus_result[0])
			if(volcanus_result[1]==1): #it meets the requirements
				if((media) > 40 and (media < 90) ):
					if(media > 65):
						#print("e0")
						healty=-1
					else:
						healty=1
				
		elif(len(volcanus_result)==4):
			#print(MAF(volcanus_result[0]), volcanus_result[1], MAF(volcanus_result[2]), volcanus_result[3])
			media1 = MAF(volcanus_result[0])
			qflag1 = volcanus_result[1]
			media2 = MAF(volcanus_result[2])
			qflag2 = volcanus_result[3]
			
			if(qflag1==1):
				#print("e1")
				if((media1) > 40 and (media1 < 90) ):
					if(media1 > 65):
						healty=-1
					else:
						healty=1			
			if(qflag2==1 and healty==1):
				#print("e2")
				if((media1) > 40 and (media1 < 90) ):
					if(media1 > 65):
						healty=-1
					else:
						healty=1

		return healty
	
	elif(application[2]=='B'): #essa e a BM
		if(numpy.random.randint(2)==1):
			healty=1
		else:
			healty=-1

		if(len(volcanus_result)==2): #passar
			media = MAF(volcanus_result[0])
			if(volcanus_result[1]==1):
				if(media > 144):
					healty = -1;
				else:
					healty=1

		elif(len(volcanus_result)==4):
			#print(MAF(volcanus_result[0]), volcanus_result[1], MAF(volcanus_result[2]), volcanus_result[3])
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



def calcula_statisticas(healty_oplm, healty_bm):
	situacaoEsperadaLinha = 99
	situacaoEsperadaBateria = 99
	
	global acertoBateria 
	global erroBateria
	global acertoLinha
	global erroLinha

	#VP VN FP FN da bateria
	global truePositive_bm
	global trueNegative_bm
	global falsePositive_bm
	global falseNegative_bm

	#VP VN FP FN da linha
	global truePositive_oplm
	global trueNegative_oplm
	global falsePositive_oplm
	global falseNegative_oplm
	
	if(situation==1):
		situacaoEsperadaLinha = 1
		situacaoEsperadaBateria = 1
	elif(situation==2):
		situacaoEsperadaLinha = -1
		situacaoEsperadaBateria = 1
	elif(situation==3):
		situacaoEsperadaLinha = 1
		situacaoEsperadaBateria = -1
	elif(situation==4):
		situacaoEsperadaLinha = -1
		situacaoEsperadaBateria = -1

	
	if (healty_bm == situacaoEsperadaBateria):
		acertoBateria = acertoBateria + 1
		if (healty_bm == 1):
			truePositive_bm = truePositive_bm + 1
		else:
			trueNegative_bm = trueNegative_bm + 1

	else:
		erroBateria = erroBateria + 1
		if (healty_bm == 1):
			falsePositive_bm = falsePositive_bm + 1
		else:
			falseNegative_bm = falseNegative_bm + 1


	if (healty_oplm == situacaoEsperadaLinha):
		acertoLinha = acertoLinha + 1
		if (healty_oplm == 1):
			truePositive_oplm = truePositive_oplm + 1
		else:
			trueNegative_oplm = trueNegative_oplm + 1

	else:
		erroLinha = erroLinha + 1
		if (healty_oplm == 1):
			falsePositive_oplm = falsePositive_oplm + 1
		else:
			falseNegative_oplm = falseNegative_oplm + 1

 

resultados_de_acuracia_oplm = []
resultados_de_acuracia_bm = []
resultados_de_acuracia_conjunto2apps = []


resultados_de_VP_oplm= []
resultados_de_VN_oplm= []
resultados_de_FP_oplm= []
resultados_de_FN_oplm= []

resultados_de_VP_bm= []
resultados_de_VN_bm= []
resultados_de_FP_bm= []
resultados_de_FN_bm= []


times=[]

repeticoes_experimento=29#0
while repeticoes_experimento < 30:
	
	rodada = 1
	while rodada < 30:#000:
	
		FW=populate_FW()
	
		FW.sort()
	
		healty_oplm = []
		healty_bm = []
		
		inicio=datetime.datetime.now().microsecond
		
		if(Run=='V'):
			healty_oplm=applicationEvaluation(Volcanus_main(FW, application1), application1)
			healty_bm=applicationEvaluation(Volcanus_main(FW, application2), application2)
		else:	
			healty_oplm=applicationEvaluation((FW,1),  application1)
			healty_bm=applicationEvaluation((FW,1),  application2)
		
		fim=datetime.datetime.now().microsecond
		elapsedTime=fim - inicio
		print(elapsedTime)
		times.append(elapsedTime)
		calcula_statisticas(healty_oplm, healty_bm)
		
		rodada=rodada+1

	repeticoes_experimento=repeticoes_experimento+1

	resultados_de_acuracia_oplm.append((acertoLinha / (acertoLinha + erroLinha )) * 100.0)	
	resultados_de_acuracia_bm.append((acertoBateria / (acertoBateria + erroBateria )) * 100.0)
	resultados_de_acuracia_conjunto2apps.append((((acertoLinha / (acertoLinha + erroLinha )) * 100.0) + ((acertoBateria / (acertoBateria + erroBateria )) * 100.0))/2)

	resultados_de_VP_oplm.append(truePositive_oplm)
	resultados_de_VN_oplm.append(trueNegative_oplm)
	resultados_de_FP_oplm.append(falsePositive_oplm)
	resultados_de_FN_oplm.append(falseNegative_oplm)

	resultados_de_VP_bm.append(truePositive_bm)
	resultados_de_VN_bm.append(trueNegative_bm)
	resultados_de_FP_bm.append(falsePositive_bm)
	resultados_de_FN_bm.append(falseNegative_bm)


	#print("OPLM: ",numpy.mean(resultados_de_acuracia_oplm), numpy.std(resultados_de_acuracia_oplm), mean_confidence_interval(resultados_de_acuracia_oplm, confidence=0.99))
	#print("BM: ",numpy.mean(resultados_de_acuracia_bm), numpy.std(resultados_de_acuracia_bm), mean_confidence_interval(resultados_de_acuracia_bm, confidence=0.99))
	#print("Conjunto das 2 apps: ",numpy.mean(resultados_de_acuracia_conjunto2apps), numpy.std(resultados_de_acuracia_conjunto2apps), mean_confidence_interval(resultados_de_acuracia_conjunto2apps, confidence=0.99))
	print(numpy.mean(times), numpy.std(times), mean_confidence_interval(times, confidence=0.99))

	#statistics for evaluation
	acertoBateria = 0.0
	erroBateria =  0.0
	acertoLinha =  0.0
	erroLinha =  0.0

	#VP VN FP FN da bateria
	truePositive_bm =  0.0
	trueNegative_bm =  0.0
	falsePositive_bm =  0.0
	falseNegative_bm =  0.0

	#VP VN FP FN da linha
	truePositive_oplm =  0.0
	trueNegative_oplm =  0.0
	falsePositive_oplm =  0.0
	falseNegative_oplm =  0.0

	'''acuraciaLinhaOk = (((double) acertoLinha / (double) rodadaOk) * 100.0);
	acuraciaBateriaOk = (((double) acertoBateria / (double) rodadaOk) * 100.0);'''
	#print((((acertoLinha / (acertoLinha + erroLinha )) * 100.0) + ((acertoBateria / (acertoBateria + erroBateria )) * 100.0))/2, truePositive_oplm, trueNegative_oplm, falsePositive_oplm, falseNegative_oplm, truePositive_bm, trueNegative_bm, falsePositive_bm, falseNegative_bm )	
