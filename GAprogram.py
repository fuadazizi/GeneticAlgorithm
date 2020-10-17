import random
import numpy as np
import matplotlib.pyplot as plt
population, gen = 2, 3

# Global variabel
global NKromosom
global sum_pop
global c

#NKromosom = 8
#c = 3
#sum_pop =5

class Individu:
	a = 3
	arr_chrom = []
	x1, x2 = 0, 0
	h = 0
	fitness = 0

	def __init__(self,chrom):
		self.arr_chrom = chrom
		'''chrom = [] 
		for i in range(10):
			biner = random.randint(0,1)
			chrom.append(biner)
		arr_chrom = chrom'''
		self.CountAttr()

	def convertX1(self):
		a = 2
		b = -1
		N = len(self.arr_chrom)/2
		multiple = 0
		suma = 0
		temp = 0

		for i in range(int(N)):
			temp = pow(2, (-i-1))										# cari nilai pembagi sum of 2^-i 1-N
			suma = suma + temp
			multiple = multiple + (self.arr_chrom[i]*temp)				# cari nilai pengkali multiple g1.2^-1+...
		self.x1 = b + (((a-b)/suma) * multiple)							

	def convertX2(self):
		a = 1
		b = -1
		N = len(self.arr_chrom)
		multiple = 0
		suma = 0
		temp = 0

		for i in range(int(N/2),N):
			temp = pow(2, (-i-1))										# cari nilai pembagi sum of 2^-i 1-N
			suma = suma + temp
			multiple = multiple + (self.arr_chrom[i]*temp)				# cari nilai pengkali multiple g1.2^-1+...

		self.x2 = b + (((a-b)/suma) * multiple)

	def fungsiH(self):
		x1 = self.x1
		x2 = self.x2
		cosx1 = np.cos(x1)
		sinx2 = np.sin(x2)
		self.h = cosx1 * sinx2 - (x1/(x2*x2+1))							# hitung fungsi H

	def hitungFitness(self):
		h = self.h
		a = self.a
		self.fitness = 1/(h+a)

	def CountAttr(self):
		self.convertX1()
		self.convertX2()
		self.fungsiH()
		self.hitungFitness()

	def printIndividu(self):
		print(self.arr_chrom,end='')
		'''print("x1: ",self.x1)
		print("x2: ",self.x2)
		print("Fitness: ",self.fitness)'''

	def mutate(self, pm):
		for i in range (len(self.arr_chrom)):
			if random.random() <= pm:									# cek apakah suatu kromosom dimutasi atau tidak tergantung pm
				if self.arr_chrom[i] == 1:
					self.arr_chrom[i] = 0
				else:
					self.arr_chrom[i] = 1
		self.CountAttr();

	def crossover(self, ind1, ind2, anakKe):							# crossover dengan uniform crossover
		pola = []
		for i in range(len(self.arr_chrom)):
			pola.append(random.randint(0,1))							# membuat pola untuk crossover	
		if anakKe == 1:
			for i in range(len(pola)):
				if pola[i] == 0:
					self.arr_chrom[i] = ind1.arr_chrom[i]
				else:
					self.arr_chrom[i] = ind2.arr_chrom[i]
		else:
			for i in range(len(pola)):
				if pola[i] == 1:
					self.arr_chrom[i] = ind1.arr_chrom[i]
				else:
					self.arr_chrom[i] = ind2.arr_chrom[i]			
		self.CountAttr()

class Populasi():
	arr_individu = []
	bestIndividu = 0
	sum_pop = 20
	sum_fitness = 0
	NKromosom = 10

	def __init__(self, newChrom):
		if (newChrom == None):
			for idx in range(self.sum_pop):
				chrom = []
				for i in range(10):
					biner = random.randint(0,1)
					chrom.append(biner)
				#chrom = Individu()
				self.arr_individu.append(Individu(chrom))
		else:
			self.arr_individu = newChrom
		self.sortPopulasi()
		self.bestIndividu = self.arr_individu[0]

	def TotalFitness():
		for individu in range(arr_individu):
			sum_fitness += arr_individu.fitness

	def sortPopulasi(self):
		currentBest, temp = 0, 0
		sum_pop = self.sum_pop
		for loop in range(sum_pop-1):
			currentBest = loop
			i = loop + 1
			for i in range(loop+1,sum_pop):
				if (self.arr_individu[currentBest].fitness < self.arr_individu[i].fitness):
					currentBest = i
			temp = self.arr_individu[currentBest]
			self.arr_individu[currentBest] = self.arr_individu[loop]
			self.arr_individu[loop] = temp

	def printPopulasi(self):
		for individu in self.arr_individu:
			individu.printIndividu()
		print()

	def Regenerasi(self):
		elite = 0.2
		doMutate = 0.5
		pm = 0.4
		size = 0
		#sizeInduk = 0
		sizeInduk = int(self.sum_pop * elite)
		nextGen = []

		# PEMILIHAN ORANG TUA
		for i in range(sizeInduk):
			nextGen.append(self.Copy(self.arr_individu[i]))

		size = sizeInduk

		sama = []
		while sizeInduk < size + (self.sum_pop * elite):
			select = random.randint(size,(self.sum_pop-1))
			if (not self.isSama(sama,select)):
				if (random.uniform(0,self.sum_fitness) <= self.arr_individu[select].fitness):
					nextGen.append(self.Copy(self.arr_individu[select]))
					sizeInduk+=1
					sama.append(select)

		size = sizeInduk

		# LAKUKAN REKOMBINASI
		while (size < sizeInduk*2):
			rand1 = random.randint(0,sizeInduk)
			rand2 = random.randint(0,sizeInduk)
			if (rand1 != rand2):
				induk1 = self.arr_individu[rand1]
				induk2 = self.arr_individu[rand2]
				anak1 = self.Copy(self.arr_individu[rand1])
				anak2 = self.Copy(self.arr_individu[rand2])

				anak1.crossover(induk1,induk2,1)
				anak2.crossover(induk1,induk2,2)
				nextGen.append(anak1)
				nextGen.append(anak2)
				size += 2

		# LAKUKAN MUTASI
		while(size < self.sum_pop):
			randind = random.randint(0,sizeInduk)
			if (random.random() <= doMutate):
				anak = self.Copy(nextGen[randind])
				anak.mutate(pm)
				nextGen.append(anak)
				size+=1

		nextPop = Populasi(nextGen)
		return nextPop

	def isSama(self, sama, someInt):
		for i in range(len(sama)):
			if (sama[i] == someInt): return True
		return False

	def Copy(self, main):
		clone = []
		for i in range(len(main.arr_chrom)):
			clone.append(main.arr_chrom[i])
		return Individu(clone)

# ================================ MAIN ================================

sum_gen = 20
Gen = [] 
population = Populasi(None)
AllBest=[]
Indeks=[]
i=0

print("  Gen\t||             Kromosom           ||\t x1\t\t||\t\tx2\t\t||   Fitness   ||     h    ")
print("_________________________________________________________________________________________________")
for i in range(sum_gen):
	Gen.append(population)
	best = Gen[i].bestIndividu
	print("  ",i+1,"\t|| ",end='')
	best.printIndividu()
	print(" ||\t ",end='')
	print(round(best.x1,3),"\t||\t  ",round(best.x2,3)," \t||\t",round(best.fitness,3),"  ||", round(best.h,6))
	##Gen[i].printPopulasi()
	population = Gen[i].Regenerasi()
	AllBest.append(best.fitness)
	Indeks.append((i+1))

print()
print("Kesimpulan Individu terbaik")
print("kromosom 	  : ", end="")
best.printIndividu() 
print()
print("Nilai x1 	  :",best.x1)
print("Nilai x2 	  :",best.x2)
print("Nilai h(x1,x2):",best.h)


# PREVIEW GRAFIK
'''plt.plot(Indeks,AllBest)
plt.title("Grafik fitness terbaik tiap generasi")
plt.xlabel("# Gen")
plt.ylabel("Fitness value")
plt.show()'''