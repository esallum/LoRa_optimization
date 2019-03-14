

#_________________________________________________________________________________________________________________________
#valores originais em segundos::
# packet transmission time at given SF
# (seconds; assuming an average payload size of 10 bytes)
#T_SF={"SF7": 0.056, "SF8": 0.103, "SF9": 0.205, "SF10": 0.371, "SF11": 0.741, "SF12": 1.483}

#_________________________________________________________________________________________________________________________
#segundos:

# Valores correspondentes ao LoRASIM (tamanho Pacote: 10bytes, CR = 4, BW = 125mhz):
#T_SF={"SF7": 0.0535, "SF8": 0.090624, "SF9": 0.181248, "SF10": 0.362496, "SF11": 0.724992, "SF12": 1.18784} #em segundos


#1 hora = 3600000 milisegundos
#avgSendTime = 600000 # milisegundos

#converter para segundos
#avgSendTime = avgSendTime / 1000 


# average transmission rate (1/tx interval in seconds)
#L = 1/avgSendTime # 1/900 corresponde a 15 minutos (900.000 milisegundos)

#_________________________________________________________________________________________________________________________
#milisegundos:


# available CFs
#CF=("CF1", "CF2", "CF3", "CF4", "CF5", "CF6", "CF7", "CF8", "CF9") 
CF=("CF1", "CF2", "CF3", "CF4", "CF5", "CF6", "CF7", "CF8") 

# available SFs
SF=("SF7", "SF8", "SF9", "SF10", "SF11", "SF12")

#Valores correspondentes ao LoRASIM (tamanho Pacote: 20bytes, CR = 1, BW = 125mhz and low data rate optimization mandated for BW125 with SF11 and SF12):
T_SF={"SF7": 56.57600000000001, "SF8": 102.912, "SF9": 185.344, "SF10": 370.688, "SF11": 741.376, "SF12": 1318.912} #em milisegundos

avgSendTime = 1000000 # milisegundos

L = 1/avgSendTime 

# g sub-band
G=("CF4", "CF5", "CF6", "CF7", "CF8")
# g1 sub-band
G1=("CF1", "CF2", "CF3")
# g2 sub-band
#G2=("CF9")
