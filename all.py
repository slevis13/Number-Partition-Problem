import random
import copy
import math
import time

def KK(A):
    S = copy.copy(A)
    residue = 0
    while True:
        a = max(S)
        i = S.index(a)
        S[i] = 0
        b = max(S)
        if b == 0:
            break
        j = S.index(b)
        S[i] = abs(a - b)
        S[j] = 0
        residue = S[i]
    return residue

def gen_instance(size):
    r_max = 10**12
    return [random.randint(1, r_max) for i in range(size)]

#RepRandom -- Stan
def rand_soln_stan(size):
    S = []
    for i in range(size):
        s = 1 if (random.random() < 0.5) else -1
        S.append(s)
    return S

def stan_res(size, A, S):
    residue = 0
    for i in range(size):
        residue += A[i] * S[i]
    return abs(residue)

def rept_rand_stan(size, A, max_iter, start):
    S = start
    for i in range(max_iter):
        S_1 = rand_soln_stan(size)
        if stan_res(size, A, S_1) < stan_res(size, A, S):
            S = S_1
    return stan_res(size, A, S)

#RepRandom -- PP
def rand_soln_pp(size):
    P = []
    for i in range(size):
        p = int(random.random() * size)
        P.append(p)
    return P

def new_A(size, P, A):
    A_prime = copy.copy(A)
    for j in range(size):
        if P[j] != j:
            temp = A[j]
            A_prime[P[j]] += temp
            A_prime[j] -= temp
    return A_prime
    
    

def rept_rand_pp(size, A, max_iter, start):
    S = new_A(size, start, A)
    for i in range(max_iter):
        S_1 = new_A(size, rand_soln_pp(size), A)
        if KK(S_1) < KK(S):
            S = S_1
    return KK(S)

#HillClimb -- Stan
def rand_neighbor_stan(size, S):
    X = copy.copy(S)
    i = int(random.random() * size)
    j = int(random.random() * size)
    while i == j:
        j = int(random.random() * size)
    X[i] *= -1 
    if (random.random() < 0.5):
        X[j] *= -1
    return X
            
def hill_climb_stan(size, A, max_iter, start):
    S = start
    res_0 = stan_res(size, A, S)
    for x in range(max_iter):
        S_1 = rand_neighbor_stan(size, S)
        res_1 = stan_res(size, A, S_1)
        if res_1 < res_0:
            S = S_1
            res_0 = stan_res(size, A, S)
    return stan_res(size, A, S)

# HillClimb -- PP
def rand_neighbor_pp(size, P):
    X = copy.copy(P)
    i = int(random.random() * size)
    j = int(random.random() * size)
    while P[i] == j:
        j = int(random.random() * size)
    X[i] = j
    return X

def hill_climb_pp(size, A, max_iter, start):
    P = start
    S = new_A(size, P, A)
    for x in range(max_iter):
        P_1 = rand_neighbor_pp(size, P)
        S_1 = new_A(size, P_1, A)
        if KK(S_1) < KK(S):
            S = S_1
    return KK(S)

#SimAn -- Stan
def T(x):
    return (10**10)*(0.8 ** (x/300))

def sim_anneal_stan(size, A, max_iter, start):
    S = start
    S_2 = copy.copy(S)
    for i in range(max_iter):
        S_1 = rand_neighbor_stan(size, S) 
        res_0 = stan_res(size, A, S)
        res_1 = stan_res(size, A, S_1)
        if res_1 < res_0:
            S = S_1
        elif random.random() < math.exp(-(res_1 - res_0)/T(i)):
            S = S_1
        if stan_res(size, A, S) < stan_res(size, A, S_2):
            S_2 = copy.copy(S)
    return stan_res(size, A, S_2)

#SimAn -- PP
def sim_anneal_pp(size, A, max_iter, start):
    P = start
    P_2 = copy.copy(P)
    res_0 = KK(new_A(size, P, A))
    res_2 = KK(new_A(size, P_2, A))
    for i in range(max_iter):
        P_1 = rand_neighbor_pp(size, P)
        res_1 = KK(new_A(size, P_1, A))
        if res_1 < res_0:
            P = P_1
            res_0 = KK(new_A(size, P, A))
        elif random.random() < math.exp(-(res_1 - res_0)/T(i)):
            P = P_1
            res_0 = KK(new_A(size, P, A))
        if res_0 < res_2:
            P_2 = copy.copy(P)
            res_2 = KK(new_A(size, P_2, A))
    return KK(new_A(size, P_2, A))


def main():
    start_all = time.time()
    
    random.seed()
    size = 100
    max_iter = 2500
    trials = 50
    
    RR_stan = 0
    RR_pp = 0
    KK_sum = 0
    HC_stan = 0
    HC_pp = 0
    SA_stan = 0
    SA_pp = 0

    KK_time = 0
    RR_stan_time = 0
    RR_pp_time = 0
    HC_stan_time = 0
    HC_pp_time = 0
    SA_stan_time = 0
    SA_pp_time = 0

    for i in range(trials):
        stan_start = rand_soln_stan(size)
        pp_start = rand_soln_pp(size)
        
        instance = gen_instance(size)

        #KK 
        start = time.time()
        KK_sum += KK(instance)
        end = time.time()
        KK_time += (end - start)
        
        #RR_stan
        start = time.time()
        RR_stan += rept_rand_stan(size, instance, max_iter, stan_start)
        end = time.time()
        RR_stan_time += (end - start)
        
        #RR_pp
        start = time.time()
        RR_pp += rept_rand_pp(size, instance, max_iter, pp_start)
        end = time.time()
        RR_pp_time += (end - start)

        #HC_stan
        start = time.time()
        HC_stan += hill_climb_stan(size, instance, max_iter, stan_start)
        end = time.time()
        HC_stan_time += (end - start)

        #HC_pp
        start = time.time()
        HC_pp += hill_climb_pp(size, instance, max_iter, pp_start)
        end = time.time()
        HC_pp_time += (end - start)

        #SA_stan
        start = time.time()
        SA_stan += sim_anneal_stan(size, instance, max_iter, stan_start)
        end = time.time()
        SA_stan_time += (end - start)

        #SA_pp
        start = time.time()
        SA_pp += sim_anneal_pp(size, instance, max_iter, pp_start)
        end = time.time()
        SA_pp_time += (end - start)

    end_all = time.time()
    time_all = end_all - start_all
    
    print("KK avg: ", int(KK_sum/trials))
    print("avg time: ", KK_time/trials)
    print("\n")
    print("RR_stan avg: ", int(RR_stan/trials))
    print("avg time: ", RR_stan_time/trials)
    print("\n")
    print("RR_pp avg: ", int(RR_pp/trials))
    print("avg time: ", RR_pp_time/trials)
    print("\n")
    print("HC_stan avg: ", int(HC_stan/trials))
    print("avg time: ", HC_stan_time/trials)
    print("\n")
    print("HC_pp avg: ", int(HC_pp/trials))
    print("avg time: ", HC_pp_time/trials)
    print("\n")
    print("SA_stan avg: ", int(SA_stan/trials))
    print("avg time: ", SA_stan_time/trials)
    print("\n")
    print("SA_pp avg: ", int(SA_pp/trials))
    print("avg time: ", SA_pp_time/trials)
    print("\n")
    
    print("time_all: ", time_all)
    
main()
