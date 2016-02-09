# Yash Shrivastava 13CS10054

from sage.all import *
from random import randint
from math import *
from tree import Tree
import setup		
import time

			
def  setup():
	alpha = Integer(Fp.random_element())
	temp_P = P
	temp_Q = Q
	# print alpha
	# alpha = Integer(alpha)
	# print alpha
	global Y_P
	global Y_Q
	global n
	for i in xrange(2*n+1):
		Y_P.append(temp_P)
		Y_Q.append(temp_Q)
		temp_P = alpha*temp_P
		temp_Q = alpha*temp_Q

# input: n -> array of number of nodes at each hierarchy level
#		 K -> number of hierarchy levels
# output: msk, (PK1, PK2) corresponding to ith user
def  keygen():
	global msk
	global PK1
	global PK2
	msk.append(Integer(Fp.random_element()))
	PK1.append(msk[-1]*P)
	PK2.append(msk[-1]*Q)

def encrypt(i1, i2, m):
	# print 'index : ', i1_, i2
	# print 'Plaintext : ', m

	t = Integer(Fp.random_element())
	# print t
	
	c1 = t*Q
	# print 'c1 : ', c1
	# print i1, i2, len(PK2), len(Y_Q)
	c2 = t*(PK2[i1])
	c4 = t*(Y_Q[i2])
	
	global n
	global PK1
	global PK2
	global Y_P
	global Y_Q
	point_order = Y_P[n].order()
	base_field_size = GF(point_order)(p).multiplicative_order()
	c3 = (Y_P[n].tate_pairing(t*Y_Q[1], point_order, base_field_size))
	# print 'c3 w/o m : ' , c3
	c3 = c3*m
	# return (c1, c2, c4, c3)
	return (c1, c2, c4, c3)


# extract for user i1
def extract(S):
	global n
	global K_S
	a1 = -1
	for (i1, i2) in S:
		if i1 != a1:
			# print i1, i2, len(K_S), len(Y_P)
			K_S[i1] = msk[i1]*Y_P[n+1-i2]
			a1 = i1
		else:
			K_S[i1] += msk[i1]*Y_P[n+1-i2]

def decrypt(C, i, K_S, S):
	# print 'decrypt'
	# c1, c2, c4, c3 = C
	c1, c2, c4, c3 = C
	# print 'c1 : ', c1
	# print 'c2 : ', c2 
	# print 'c3 : ', c3
	i1, i2 = i
	global n
	global p

	


	b_S = sum([Y_P[n+1-j2] for (i1_, j2) in S if i1_ == i1])
	# point_order = b_S.order()
	# base_field_size = GF(point_order)(p).multiplicative_order()
	# tp2 = b_S.tate_pairing(c4, point_order, base_field_size)

	


	a_S = sum([Y_P[n+1-j2+i2] for (i1_, j2) in S if i1 == i1_ and j2 != i2])
	# a_S = sum([Y_P[n+1-j2+i2] for (i1_, j2) in S if i1 == i1_])
	# point_order = a_S.order()
	# base_field_size = GF(point_order)(p).multiplicative_order()
	# tp1 = a_S.tate_pairing(c1, point_order, base_field_size)
	# if a_S - b_S == -Y_P[n + 1]:
	# 	print "Correct a_S and b_S"
	# else:
	# 	print "InCorrect a_S and b_S"
	# print '\n \n \ne(b_S, c4)/e(a_S, c1) : ', tp1/tp2
	print a_S, K_S, b_S, i1, i2
	point_order = (K_S).order()
	base_field_size = GF(point_order)(p).multiplicative_order()
	tp1 = ((K_S).tate_pairing(c1, point_order, base_field_size))
	
	point_order = a_S.order()
	base_field_size = GF(point_order)(p).multiplicative_order()
	tp2 = a_S.tate_pairing(c1, point_order, base_field_size)

	point_order = b_S.order()
	base_field_size = GF(point_order)(p).multiplicative_order()
	tp3 = b_S.tate_pairing(c4, point_order, base_field_size)

	point_order = b_S.order()
	base_field_size = GF(point_order)(p).multiplicative_order()
	tp4 = b_S.tate_pairing(c2, point_order, base_field_size)

	# print 'tp1/tp4: ', tp1/tp4
	# print tp3/tp2
	m = tp1*tp2/(tp3*tp4)
	# print 'm w/o c3 : ', m
	m = m*c3
	# point_order = b_S.order()
	# base_field_size = GF(point_order)(p).multiplicative_order()
	# m = m/(b_S.tate_pairing(c2 + c4, point_order, base_field_size))
	
	return m


def main():
	setup()

	set_random_seed(randint(1,100))


	msg = P.tate_pairing(Q, ec_order, k);
	PT = []
	for i in xrange(100):
		PT.append(Fp.random_element()*Fp.random_element()*msg)
		while PT[i] == 0:
			PT[i] = Fp.random_element()*Fp.random_element()*msg
	# for i in xrange(100):
	# 	print i, PT[i]
	for run in xrange(10):
		print '\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
		CT = [None]*100
		DT = [None]*100
		n1 = n_users[run]
		n2 = n_classes[run]
		global msk 
		msk = []
		time_keygen_begin = time.time()
		for i in xrange(n1):
			keygen()
		# msg += msg
		time_keygen_end = time.time()

		S = []
		for j in xrange(n_tests):
			index = randint(1,n)
			i1 = index/n2
			i2 = index%n2
			S.append([i1,i2])

		S = sorted(S, key = lambda index : index[0])
		print 'Subset S : \n', S
		global K_S
		K_S = [None]*n1
		extract(S)
		print 'Aggregate Key K_S : \n', K_S

		time_encrypt_begin = time.time()
		for (i1, i2) in S:
			CT[i1*n2+i2] = encrypt(i1, i2, PT[i1*n2+i2])
		time_encrypt_end = time.time()
		
		time_decrypt_begin = time.time()
		for (i1, i2) in S:
			DT[i1*n2+i2] = decrypt(CT[i1*n2 + i2], (i1, i2), K_S[i1], S)
		time_decrypt_end = time.time()


		for (i1, i2) in S:
			index = i1*n2 + i2
			print 'index : ', i1, ',' ,i2
			print 'Plaintext : \n', PT[index]
			print 'encryption : \n', CT[index]
			print 'decryption : \n', DT[index]
			if DT[index] != PT[index]:
				print 'Decryption Failed'
			else:
				print 'Decryption Passed'
			print '\n \n'
		print '\n===================================================================================='
		print '====================================================================================\n'

p = 103
A = 1
B = 18
E = EllipticCurve(GF(p), [A, B])
Fp = GF(p)
# choosing P and Q
P = E(33, 91)
ec_order = P.order()
k = GF(ec_order)(p).multiplicative_order()
# P.tate_pairing(P, ec_order, k)
# Q = E(87, 51)
# P.tate_pairing(Q, ec_order, k)
set_random_seed(35)
# P.tate_pairing(P,ec_order,k)
K = GF(p**k,'a')
EK = E.base_extend(K)
P = EK(P)
Qx = 69*a**5 + 96*a**4 + 22*a**3 + 86*a**2 + 6*a + 35
Qy = 34*a**5 + 24*a**4 + 16*a**3 + 41*a**2 + 4*a + 40
Q = EK(Qx, Qy);
# multiply by cofactor so Q has order n:
h = 551269674; Q = h*Q
P = EK(P)

Y_P = []
Y_Q = []
msk = []
PK1 = []
PK2 = []
K_S = []
n = 100
n_users = [1, 2, 4, 5, 10, 20, 25, 50, 100]
n_classes = []
n_tests = 10
length = len(n_users)
for i in xrange(length):
	n_classes.append(n/n_users[i])
main();