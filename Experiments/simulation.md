We can run the above circuits in the simulator. This will gives us the results of Bob's measurements using his random basis, in both cases
(with or without eavesdropping). If there is no noise or interference by Eve, then Bob's measurements should match up precisely with Alice's
key α, at the qubits where Alice and Bob both chose the same basis. Hence, we can take this subset of Bob's measurement to use as check bits and key bits.

We also show the probabilities of various outcomes Bob could see, which are computed by simulating the above circuit using the same `a`, `b`, 
and b', 2^10 times noting the number of occurences of each outcome.

```python
def testCircuits(shots, key_length):
    # use local qasm simulator
    backend = 'ibmqx_hpc_qasm_simulator'
    qp, a, b, b_prime = BB84Program(key_length)
    
    print("Simulating...")
    
    results = qp.execute(["BB84"], backend=backend, timeout=600, shots=shots)
    answer = results.get_counts("BB84")
    
    results_eve = qp.execute(["BB84-Eve"], backend=backend, timeout=600, shots=shots)
    answer_eve = results_eve.get_counts("BB84-Eve")
    
    return (answer, answer_eve, a, b, b_prime)

(answer, answer_eve, a, b, b_prime) = testCircuits(2**10, 4)
print("Discrete distribution of potential measurements by Bob: ", answer)
print("Discrete distribution of potential measurements by Bob with eavesdropping: ", answer_eve)

```
Alice has generated random secret data bits, a:  [1 0 1 0 0 1 0 1 1 1 1 0 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 1 0 0 0 1 0 0 1 0 1]
Bob has chosen random basis, b':  [1 0 1 1 1 1 1 0 1 0 1 1 1 1 0 0]
Eve has chosen random basis:  [0 0 0 1 1 0 1 1 1 0 0 1 0 0 0 0]
Simulating...
Discrete distribution of potential measurements by Bob:  {'0000011010101101': 19, '0000111010110101': 16, '0000111010100101': 19, '1000111110100101': 10, '0000011110101101': 16, '0001111110111101': 16, '0001111010100101': 17, '0001111010110101': 16, '0001011010101101': 22, '1001111010101101': 14, '1000011110110101': 20, '0000011010110101': 20, '0000111110111101': 20, '1000111110110101': 14, '1000111110101101': 13, '0001011110101101': 10, '0001011110110101': 21, '0000111110100101': 23, '0000111110110101': 8, '1001011110101101': 14, '1000111110111101': 12, '1000011010101101': 16, '0001111110110101': 18, '0001111110100101': 16, '1001011110100101': 15, '1001111110111101': 15, '0000011010100101': 10, '0001111010101101': 16, '0001011110100101': 18, '1001111010100101': 12, '1001111010110101': 18, '0001011110111101': 13, '0000011110111101': 14, '0001111010111101': 13, '0001011010111101': 14, '1000111010110101': 18, '1001111010111101': 24, '1000011110111101': 16, '1001011010101101': 12, '0000111010111101': 12, '1001011110110101': 23, '1000111010101101': 12, '0000011110100101': 18, '1001011110111101': 14, '0001011010100101': 18, '1000111010111101': 16, '0001011010110101': 13, '1001111110100101': 12, '1000011110101101': 22, '1001011010100101': 13, '0001111110101101': 18, '1000111010100101': 14, '1001011010111101': 22, '1001111110101101': 22, '0000011010111101': 15, '0000111110101101': 25, '1001011010110101': 17, '1000011010110101': 13, '1000011010100101': 15, '0000011110110101': 22, '1000011110100101': 11, '0000111010101101': 10, '1000011010111101': 12, '1001111110110101': 17}
Discrete distribution of potential measurements by Bob with eavesdropping:  {'1000011101100101': 63, '1001011101100101': 53, '0001011100100101': 84, '1001011100100101': 61, '1001011110100101': 55, '0001011101100101': 68, '0000011101100101': 71, '0001011111100101': 56, '0000011100100101': 69, '1000011111100101': 65, '1001011111100101': 65, '0000011110100101': 61, '1000011110100101': 56, '0000011111100101': 64, '0001011110100101': 62, '1000011100100101': 71}

Of course, Bob will not see a probability distribution, but rather one of these particular outcomes. Hence, we'll take one of these outcomes at random.
```
def getMeasurement(answer, answer_eve):
    bob_meas = list(random.choice(list(answer.keys())))
    bob_meas = list(map(int, bob_meas))
    bob_meas = np.array(bob_meas)
    bob_meas = bob_meas[::-1]
    print("Bob's measurement result: ", bob_meas)
    
    bob_meas_eve = list(random.choice(list(answer_eve.keys())))
    bob_meas_eve = list(map(int, bob_meas_eve))
    bob_meas_eve = np.array(bob_meas_eve)
    bob_meas_eve = bob_meas_eve[::-1]
    print("Bob's measurement result with eavesdropping: ", bob_meas_eve)
    
    return (bob_meas, bob_meas_eve)
    
bob_meas, bob_meas_eve = getMeasurement(answer, answer_eve)
```
Bob's measurement result:  [1 0 1 1 0 1 0 1 1 1 1 0 0 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 1 1 0 1 1 1 0 1 0 0 0]
Now, we can use the above measurement to determine whether the key exchange was successful or not. In other words, Alice and Bob determine if their check bits agree in enough places so that they can conclude that their was no interference by Eve.

First, they communicate over a classical channel to determine where their choices in random bases agreed.
```
print("Key Exchange without eavesdropping: ")
res = determineKey(a, bob_meas, b, b_prime)
print("Key Exchange with eavesdropping: ")
res = determineKey(a, bob_meas_eve, b, b_prime)
```
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Hence, we can perform the above steps over many iterations to observe expirementally how likely Alice and Bob are to succeed in key 
exchange in addition to how likely Eve is to eavesdrop undetected.
```
def plot_eve_undetected(probs):
    
    objects = ('2', '4', '8')
    y_pos = np.arange(len(objects))
    
    plt.bar(y_pos, probs, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    
    plt.xlabel("Key Length")
    plt.ylabel('Probability')
    plt.title('Probability of Undetected Eavesdropping')
    
    plt.show()
```
----------------------------------------------------------------------
```
probs = []

for n in [2, 4, 8]:
    succ = 0
    succ_eve = 0
    for i in range(2**7):
        print("Simulation round:", i)
        # Simulate one measurement with key length n = 4
        (answer, answer_eve, a, b, b_prime) = testCircuits(1, n)
        bob_meas, bob_meas_eve = getMeasurement(answer, answer_eve)
        print("Key Exchange without eavesdropping: ")
        res = determineKey(a, bob_meas, b, b_prime)
        # successful
        if res: 
            succ += 1
        print("Key Exchange with eavesdropping: ")
        res = determineKey(a, bob_meas_eve, b, b_prime)
        # successful
        if res: 
            succ_eve += 1
        
    print("n=", n)
    print("Successful key exchanges without Eve present: ", succ)
    print("Successful key exchanges with Eve present: ", succ_eve)
    p = (succ_eve) / (2**7)
    probs.append(p)
    
plot_eve()
```
---------------------------------------------------------------------

Simulation round: 0
Alice has generated random secret data bits, a:  [0 0 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 0 0 0]
Bob has chosen random basis, b':  [1 0 0 0 0 0 0 0]
Eve has chosen random basis:  [1 1 1 0 1 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 0 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 1
Alice has generated random secret data bits, a:  [0 1 0 1 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 1 0 1]
Bob has chosen random basis, b':  [1 1 1 1 1 1 0 1]
Eve has chosen random basis:  [0 1 0 0 1 0 0 1]
Simulating...
Bob's measurement result:  [1 1 1 1 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 2
Alice has generated random secret data bits, a:  [0 0 0 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 0 1 1]
Bob has chosen random basis, b':  [0 1 0 1 0 0 1 1]
Eve has chosen random basis:  [1 0 1 0 0 1 0 1]
Simulating...
Bob's measurement result:  [0 0 0 1 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Simulation round: 3
Alice has generated random secret data bits, a:  [1 0 0 0 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 1 0]
Bob has chosen random basis, b':  [0 1 1 1 1 0 0 1]
Eve has chosen random basis:  [1 1 0 1 0 1 0 0]
Simulating...
Bob's measurement result:  [1 0 1 1 0 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 4
Alice has generated random secret data bits, a:  [1 0 0 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 0 1 0]
Bob has chosen random basis, b':  [1 0 0 1 0 1 1 0]
Eve has chosen random basis:  [1 0 1 0 0 0 0 1]
Simulating...
Bob's measurement result:  [1 0 0 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 5
Alice has generated random secret data bits, a:  [1 1 1 1 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 0 0 1]
Bob has chosen random basis, b':  [1 1 0 1 1 1 0 1]
Eve has chosen random basis:  [1 1 1 1 1 0 0 0]
Simulating...
Bob's measurement result:  [0 1 1 1 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Simulation round: 6
Alice has generated random secret data bits, a:  [0 1 0 1 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 0 0 1]
Bob has chosen random basis, b':  [1 1 1 1 1 1 1 1]
Eve has chosen random basis:  [0 1 1 1 1 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 7
Alice has generated random secret data bits, a:  [0 0 0 0 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 1 1 0]
Bob has chosen random basis, b':  [1 0 0 0 1 0 0 1]
Eve has chosen random basis:  [0 1 0 0 1 0 1 0]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 8
Alice has generated random secret data bits, a:  [1 0 1 1 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 0 1 0]
Bob has chosen random basis, b':  [0 0 0 1 0 1 1 1]
Eve has chosen random basis:  [1 0 0 1 1 1 1 0]
Simulating...
Bob's measurement result:  [1 1 1 1 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Simulation round: 9
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 0 1 0]
Bob has chosen random basis, b':  [1 1 1 0 1 0 0 0]
Eve has chosen random basis:  [0 1 0 0 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 0 1 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Simulation round: 10
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 0 1]
Bob has chosen random basis, b':  [1 1 0 0 1 0 1 0]
Eve has chosen random basis:  [1 1 1 1 0 1 0 0]
Simulating...
Bob's measurement result:  [0 0 0 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 1 0 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 11
Alice has generated random secret data bits, a:  [0 1 1 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 0 0 1 1]
Bob has chosen random basis, b':  [1 1 0 0 0 0 1 1]
Eve has chosen random basis:  [0 0 0 0 1 0 1 1]
Simulating...
Bob's measurement result:  [1 1 1 0 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 12
Alice has generated random secret data bits, a:  [0 1 0 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 0 0 1]
Bob has chosen random basis, b':  [0 0 0 1 1 1 1 0]
Eve has chosen random basis:  [0 1 0 0 1 1 0 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 13
Alice has generated random secret data bits, a:  [0 0 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 1 0 1]
Bob has chosen random basis, b':  [1 1 1 0 0 1 1 1]
Eve has chosen random basis:  [0 1 1 1 1 0 0 1]
Simulating...
Bob's measurement result:  [0 1 0 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 14
Alice has generated random secret data bits, a:  [1 0 1 1 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 0 0 0 1]
Bob has chosen random basis, b':  [0 1 0 1 1 1 0 0]
Eve has chosen random basis:  [0 1 1 1 0 0 1 0]
Simulating...
Bob's measurement result:  [1 0 0 1 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Simulation round: 15
Alice has generated random secret data bits, a:  [0 0 1 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 1 0 0 0]
Bob has chosen random basis, b':  [1 1 0 0 0 0 0 1]
Eve has chosen random basis:  [1 0 0 1 1 1 0 1]
Simulating...
Bob's measurement result:  [0 0 1 1 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 16
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 0 1 0 0]
Bob has chosen random basis, b':  [0 1 0 1 0 0 0 0]
Eve has chosen random basis:  [1 1 0 0 1 0 1 0]
Simulating...
Bob's measurement result:  [1 0 0 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [1 1 0 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 17
Alice has generated random secret data bits, a:  [0 0 1 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 1 0]
Bob has chosen random basis, b':  [0 0 1 1 1 0 1 0]
Eve has chosen random basis:  [0 1 1 1 1 1 0 0]
Simulating...
Bob's measurement result:  [1 0 1 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Simulation round: 18
Alice has generated random secret data bits, a:  [1 0 1 1 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 0 1 1]
Bob has chosen random basis, b':  [1 0 0 0 0 0 0 0]
Eve has chosen random basis:  [1 0 0 1 0 0 1 1]
Simulating...
Bob's measurement result:  [1 0 1 1 0 1 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Simulation round: 19
Alice has generated random secret data bits, a:  [1 0 0 0 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 1 1 1]
Bob has chosen random basis, b':  [1 0 1 0 1 1 0 1]
Eve has chosen random basis:  [0 1 0 0 0 1 0 0]
Simulating...
Bob's measurement result:  [1 0 1 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Simulation round: 20
Alice has generated random secret data bits, a:  [1 1 1 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 1 0 0]
Bob has chosen random basis, b':  [1 0 0 1 0 0 1 1]
Eve has chosen random basis:  [0 0 0 1 0 1 0 1]
Simulating...
Bob's measurement result:  [1 1 1 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Simulation round: 21
Alice has generated random secret data bits, a:  [0 0 1 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 1 0 0]
Bob has chosen random basis, b':  [1 0 1 0 0 1 1 0]
Eve has chosen random basis:  [1 1 1 0 1 0 1 0]
Simulating...
Bob's measurement result:  [0 1 1 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 0 1 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Simulation round: 22
Alice has generated random secret data bits, a:  [0 0 0 0 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 0 0 0]
Bob has chosen random basis, b':  [1 0 0 0 1 1 1 1]
Eve has chosen random basis:  [1 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 0 0 1 1]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 23
Alice has generated random secret data bits, a:  [1 1 0 0 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 1 0 0 1]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 0]
Eve has chosen random basis:  [0 0 0 0 1 1 0 0]
Simulating...
Bob's measurement result:  [1 1 0 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Simulation round: 24
Alice has generated random secret data bits, a:  [1 1 1 0 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 1 1 1 1]
Bob has chosen random basis, b':  [1 1 1 1 1 0 0 0]
Eve has chosen random basis:  [1 0 0 0 0 0 1 1]
Simulating...
Bob's measurement result:  [1 0 1 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 25
Alice has generated random secret data bits, a:  [0 0 1 1 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 0 0 1]
Bob has chosen random basis, b':  [0 1 1 1 1 1 1 1]
Eve has chosen random basis:  [0 0 1 0 1 1 1 1]
Simulating...
Bob's measurement result:  [1 0 1 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 26
Alice has generated random secret data bits, a:  [0 0 1 1 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 0 1 1]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 0]
Eve has chosen random basis:  [1 0 1 1 0 0 0 1]
Simulating...
Bob's measurement result:  [0 1 1 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Simulation round: 27
Alice has generated random secret data bits, a:  [0 1 0 1 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 0 1 0 1]
Bob has chosen random basis, b':  [1 0 1 1 1 1 1 1]
Eve has chosen random basis:  [1 1 1 0 0 0 0 0]
Simulating...
Bob's measurement result:  [0 0 0 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Simulation round: 28
Alice has generated random secret data bits, a:  [0 1 1 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 0 0 0 0]
Bob has chosen random basis, b':  [1 0 1 0 0 1 1 1]
Eve has chosen random basis:  [1 1 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Simulation round: 29
Alice has generated random secret data bits, a:  [1 0 0 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 0 1 1]
Bob has chosen random basis, b':  [1 1 0 0 0 0 1 0]
Eve has chosen random basis:  [0 1 1 1 0 1 1 1]
Simulating...
Bob's measurement result:  [1 1 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 30
Alice has generated random secret data bits, a:  [1 0 1 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 0 0 0 0]
Bob has chosen random basis, b':  [0 1 1 0 0 1 0 1]
Eve has chosen random basis:  [0 0 1 0 1 0 1 1]
Simulating...
Bob's measurement result:  [0 0 1 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 31
Alice has generated random secret data bits, a:  [1 1 0 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 0 1 1]
Bob has chosen random basis, b':  [0 0 1 1 0 0 1 1]
Eve has chosen random basis:  [1 0 1 0 1 0 0 0]
Simulating...
Bob's measurement result:  [1 1 0 0 0 0 1 1]
Bob's measurement result with eavesdropping:  [1 1 1 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Simulation round: 32
Alice has generated random secret data bits, a:  [1 1 1 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 1 1 0]
Bob has chosen random basis, b':  [0 1 1 1 1 0 1 1]
Eve has chosen random basis:  [1 0 1 1 1 0 0 0]
Simulating...
Bob's measurement result:  [1 0 0 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Simulation round: 33
Alice has generated random secret data bits, a:  [1 1 1 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 1 1 1]
Bob has chosen random basis, b':  [1 0 0 0 1 0 1 1]
Eve has chosen random basis:  [0 0 0 0 1 0 0 1]
Simulating...
Bob's measurement result:  [0 1 1 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Simulation round: 34
Alice has generated random secret data bits, a:  [1 0 1 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 0 0 0 1]
Bob has chosen random basis, b':  [1 1 1 0 1 0 1 1]
Eve has chosen random basis:  [0 1 1 0 0 1 1 0]
Simulating...
Bob's measurement result:  [1 0 0 1 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 35
Alice has generated random secret data bits, a:  [1 1 1 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 0 0 0]
Bob has chosen random basis, b':  [1 0 0 1 0 1 1 1]
Eve has chosen random basis:  [1 1 0 1 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 1 1 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 1 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 36
Alice has generated random secret data bits, a:  [0 1 1 0 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 0 1 1]
Bob has chosen random basis, b':  [0 0 0 0 0 1 1 1]
Eve has chosen random basis:  [1 1 1 1 1 0 0 0]
Simulating...
Bob's measurement result:  [0 1 0 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 1 1 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Simulation round: 37
Alice has generated random secret data bits, a:  [0 0 0 1 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 1 0 1]
Bob has chosen random basis, b':  [1 1 1 1 0 1 1 1]
Eve has chosen random basis:  [1 0 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Simulation round: 38
Alice has generated random secret data bits, a:  [0 1 1 1 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 0 0 0]
Bob has chosen random basis, b':  [1 1 0 1 1 1 1 0]
Eve has chosen random basis:  [0 0 1 0 1 0 1 0]
Simulating...
Bob's measurement result:  [0 1 1 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 1 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Simulation round: 39
Alice has generated random secret data bits, a:  [1 0 1 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 1 0 0]
Bob has chosen random basis, b':  [0 0 1 1 0 1 1 0]
Eve has chosen random basis:  [1 1 1 1 1 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Simulation round: 40
Alice has generated random secret data bits, a:  [1 0 1 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 1 0 1]
Bob has chosen random basis, b':  [0 0 1 1 1 0 1 1]
Eve has chosen random basis:  [0 0 1 0 1 1 1 0]
Simulating...
Bob's measurement result:  [0 0 1 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 41
Alice has generated random secret data bits, a:  [0 1 0 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 1 0 1]
Bob has chosen random basis, b':  [0 0 1 0 1 1 1 0]
Eve has chosen random basis:  [1 0 1 1 0 0 1 0]
Simulating...
Bob's measurement result:  [1 1 0 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Simulation round: 42
Alice has generated random secret data bits, a:  [0 1 0 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 0 1 1]
Bob has chosen random basis, b':  [1 0 0 0 0 1 1 0]
Eve has chosen random basis:  [1 1 0 0 1 0 0 0]
Simulating...
Bob's measurement result:  [0 1 0 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Simulation round: 43
Alice has generated random secret data bits, a:  [1 0 0 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 0 0 0]
Bob has chosen random basis, b':  [1 0 1 0 0 1 0 0]
Eve has chosen random basis:  [0 0 1 1 1 1 1 0]
Simulating...
Bob's measurement result:  [1 0 1 1 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 44
Alice has generated random secret data bits, a:  [1 0 0 1 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 1 1 0]
Bob has chosen random basis, b':  [1 1 1 0 1 0 0 1]
Eve has chosen random basis:  [1 0 1 0 1 0 1 1]
Simulating...
Bob's measurement result:  [1 0 0 1 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 45
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 0 1 1 1]
Bob has chosen random basis, b':  [0 1 1 0 1 0 0 0]
Eve has chosen random basis:  [0 0 1 1 0 0 1 1]
Simulating...
Bob's measurement result:  [1 1 1 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Simulation round: 46
Alice has generated random secret data bits, a:  [1 0 0 1 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 0 0 1 0]
Bob has chosen random basis, b':  [1 0 1 1 1 0 0 1]
Eve has chosen random basis:  [1 1 0 1 1 1 0 1]
Simulating...
Bob's measurement result:  [1 1 0 1 0 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 0 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 47
Alice has generated random secret data bits, a:  [1 1 1 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 0 0 1 1]
Bob has chosen random basis, b':  [1 1 0 0 0 1 1 0]
Eve has chosen random basis:  [1 1 1 0 1 0 1 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Simulation round: 48
Alice has generated random secret data bits, a:  [1 1 0 1 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 1 0 1]
Bob has chosen random basis, b':  [0 1 0 0 0 0 0 1]
Eve has chosen random basis:  [0 1 1 1 0 0 1 0]
Simulating...
Bob's measurement result:  [1 0 0 1 0 0 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 49
Alice has generated random secret data bits, a:  [0 0 1 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 0 0 1]
Bob has chosen random basis, b':  [0 0 0 0 0 0 0 0]
Eve has chosen random basis:  [1 0 1 1 0 1 0 0]
Simulating...
Bob's measurement result:  [0 1 1 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Simulation round: 50
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 0 1 0 1]
Bob has chosen random basis, b':  [0 0 0 0 0 0 0 0]
Eve has chosen random basis:  [1 0 0 0 1 0 0 0]
Simulating...
Bob's measurement result:  [1 1 1 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Simulation round: 51
Alice has generated random secret data bits, a:  [0 1 1 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 1 1 0]
Bob has chosen random basis, b':  [1 0 1 1 1 1 0 0]
Eve has chosen random basis:  [0 1 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [1 1 1 1 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 52
Alice has generated random secret data bits, a:  [0 0 1 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 0 0 1]
Bob has chosen random basis, b':  [1 1 0 0 0 0 1 1]
Eve has chosen random basis:  [0 0 1 0 1 1 0 1]
Simulating...
Bob's measurement result:  [0 1 1 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 0 0 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Simulation round: 53
Alice has generated random secret data bits, a:  [0 0 1 1 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 1 1 1]
Bob has chosen random basis, b':  [1 1 1 1 1 0 0 0]
Eve has chosen random basis:  [1 0 1 1 0 0 0 0]
Simulating...
Bob's measurement result:  [1 0 1 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Simulation round: 54
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 1 0 1]
Bob has chosen random basis, b':  [0 1 0 0 0 1 1 0]
Eve has chosen random basis:  [0 1 0 1 1 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 55
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 1 0 1]
Bob has chosen random basis, b':  [1 1 1 0 1 1 1 0]
Eve has chosen random basis:  [1 1 1 0 1 0 0 0]
Simulating...
Bob's measurement result:  [1 0 1 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Simulation round: 56
Alice has generated random secret data bits, a:  [1 1 1 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 0 1 0 1]
Bob has chosen random basis, b':  [0 0 1 0 0 0 1 0]
Eve has chosen random basis:  [1 0 1 0 0 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 57
Alice has generated random secret data bits, a:  [1 0 1 1 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 1 0 1 0]
Bob has chosen random basis, b':  [1 1 1 0 1 0 1 1]
Eve has chosen random basis:  [1 0 0 0 1 0 0 1]
Simulating...
Bob's measurement result:  [1 0 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Simulation round: 58
Alice has generated random secret data bits, a:  [1 0 1 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 0 1 1]
Bob has chosen random basis, b':  [1 0 1 0 1 1 0 1]
Eve has chosen random basis:  [0 1 1 0 0 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Simulation round: 59
Alice has generated random secret data bits, a:  [1 1 0 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 1 1 0]
Bob has chosen random basis, b':  [0 0 0 0 0 0 0 1]
Eve has chosen random basis:  [0 0 0 1 0 1 1 1]
Simulating...
Bob's measurement result:  [0 1 1 0 1 1 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Simulation round: 60
Alice has generated random secret data bits, a:  [1 0 0 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 1 0 0]
Bob has chosen random basis, b':  [0 1 1 1 0 1 0 0]
Eve has chosen random basis:  [0 0 1 1 1 0 0 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Simulation round: 61
Alice has generated random secret data bits, a:  [1 0 0 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 0 1 0]
Bob has chosen random basis, b':  [0 1 0 0 1 0 1 1]
Eve has chosen random basis:  [0 0 0 0 1 0 0 0]
Simulating...
Bob's measurement result:  [1 0 0 1 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Simulation round: 62
Alice has generated random secret data bits, a:  [0 1 0 1 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 0 0 1]
Bob has chosen random basis, b':  [0 0 0 1 1 0 1 0]
Eve has chosen random basis:  [1 1 0 1 1 1 0 1]
Simulating...
Bob's measurement result:  [0 1 0 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 63
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 1 0 0 1]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 0]
Eve has chosen random basis:  [1 1 0 0 1 0 0 1]
Simulating...
Bob's measurement result:  [0 0 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Simulation round: 64
Alice has generated random secret data bits, a:  [0 0 0 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 1 0 0]
Bob has chosen random basis, b':  [0 1 1 0 1 1 1 1]
Eve has chosen random basis:  [1 1 0 0 1 0 0 1]
Simulating...
Bob's measurement result:  [0 1 1 1 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 65
Alice has generated random secret data bits, a:  [1 1 0 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 1 1 1]
Bob has chosen random basis, b':  [1 0 0 1 0 0 1 0]
Eve has chosen random basis:  [0 1 1 1 1 1 1 1]
Simulating...
Bob's measurement result:  [1 1 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 66
Alice has generated random secret data bits, a:  [1 0 1 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 0 0 0 0]
Bob has chosen random basis, b':  [1 1 1 0 1 1 0 1]
Eve has chosen random basis:  [1 1 0 1 0 1 0 1]
Simulating...
Bob's measurement result:  [1 0 1 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Simulation round: 67
Alice has generated random secret data bits, a:  [0 0 1 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 0 1 1]
Bob has chosen random basis, b':  [1 0 0 0 0 1 1 1]
Eve has chosen random basis:  [0 1 1 0 0 0 0 0]
Simulating...
Bob's measurement result:  [0 0 1 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Simulation round: 68
Alice has generated random secret data bits, a:  [1 0 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 0 0 1]
Bob has chosen random basis, b':  [1 1 1 0 1 1 0 0]
Eve has chosen random basis:  [0 1 1 1 0 1 0 1]
Simulating...
Bob's measurement result:  [1 0 0 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [0 0]
Simulation round: 69
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 1 0 0]
Bob has chosen random basis, b':  [1 1 1 1 0 1 0 1]
Eve has chosen random basis:  [0 0 1 1 1 1 1 1]
Simulating...
Bob's measurement result:  [1 1 0 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 70
Alice has generated random secret data bits, a:  [1 0 0 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 0 1 1]
Bob has chosen random basis, b':  [0 0 0 0 0 1 0 0]
Eve has chosen random basis:  [0 0 1 1 1 1 1 0]
Simulating...
Bob's measurement result:  [1 0 0 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 0 0 1 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 71
Alice has generated random secret data bits, a:  [0 1 1 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 0 1]
Bob has chosen random basis, b':  [0 1 0 1 1 1 1 1]
Eve has chosen random basis:  [1 0 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 1 0 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Simulation round: 72
Alice has generated random secret data bits, a:  [0 1 1 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 0 1 1]
Bob has chosen random basis, b':  [1 1 1 1 0 1 1 0]
Eve has chosen random basis:  [0 1 0 1 1 1 0 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 73
Alice has generated random secret data bits, a:  [1 0 0 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 1 0 0]
Bob has chosen random basis, b':  [1 1 1 1 0 0 0 0]
Eve has chosen random basis:  [0 1 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 74
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 1 1 1]
Bob has chosen random basis, b':  [1 0 0 0 0 1 0 1]
Eve has chosen random basis:  [0 0 0 1 1 1 0 0]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Simulation round: 75
Alice has generated random secret data bits, a:  [0 1 0 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 1 1 0 1]
Bob has chosen random basis, b':  [1 1 0 0 1 0 0 1]
Eve has chosen random basis:  [0 0 1 0 1 0 0 0]
Simulating...
Bob's measurement result:  [0 1 1 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Simulation round: 76
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 1 0 0]
Bob has chosen random basis, b':  [1 1 1 1 0 0 0 1]
Eve has chosen random basis:  [0 1 0 1 0 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Simulation round: 77
Alice has generated random secret data bits, a:  [1 0 0 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 0 0 0]
Bob has chosen random basis, b':  [0 0 0 1 0 1 0 1]
Eve has chosen random basis:  [1 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 78
Alice has generated random secret data bits, a:  [0 0 0 0 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 1 0 0]
Bob has chosen random basis, b':  [0 1 0 0 0 0 1 1]
Eve has chosen random basis:  [0 1 0 1 1 1 0 1]
Simulating...
Bob's measurement result:  [1 0 1 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [0]
Interference detected... Aborting!
Simulation round: 79
Alice has generated random secret data bits, a:  [1 0 0 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 1 1 0]
Bob has chosen random basis, b':  [1 1 1 0 0 0 0 0]
Eve has chosen random basis:  [0 0 1 0 1 1 1 1]
Simulating...
Bob's measurement result:  [1 0 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 80
Alice has generated random secret data bits, a:  [0 1 1 1 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 0 0 1 1]
Bob has chosen random basis, b':  [1 1 1 1 1 1 0 0]
Eve has chosen random basis:  [1 0 0 1 0 0 0 1]
Simulating...
Bob's measurement result:  [0 1 0 1 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 1 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 81
Alice has generated random secret data bits, a:  [0 0 1 1 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 1 0 0]
Bob has chosen random basis, b':  [0 1 0 0 0 1 1 1]
Eve has chosen random basis:  [0 1 1 1 1 1 0 1]
Simulating...
Bob's measurement result:  [1 1 1 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 82
Alice has generated random secret data bits, a:  [1 1 0 1 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 1 1 0]
Bob has chosen random basis, b':  [1 0 1 0 0 0 1 1]
Eve has chosen random basis:  [0 0 1 1 1 0 0 0]
Simulating...
Bob's measurement result:  [1 1 0 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Simulation round: 83
Alice has generated random secret data bits, a:  [0 0 1 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 1 0 1 1]
Bob has chosen random basis, b':  [1 0 0 1 0 1 0 1]
Eve has chosen random basis:  [1 0 1 1 1 1 0 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 84
Alice has generated random secret data bits, a:  [0 1 1 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 1 1 0]
Bob has chosen random basis, b':  [1 1 1 1 1 1 1 1]
Eve has chosen random basis:  [1 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 1 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 85
Alice has generated random secret data bits, a:  [1 1 1 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 1 1 0]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 0]
Eve has chosen random basis:  [1 0 0 1 1 1 1 1]
Simulating...
Bob's measurement result:  [1 1 1 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 86
Alice has generated random secret data bits, a:  [1 0 1 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 1 1 1]
Bob has chosen random basis, b':  [0 0 0 1 1 1 0 1]
Eve has chosen random basis:  [1 1 1 0 0 1 0 0]
Simulating...
Bob's measurement result:  [1 0 1 1 1 0 0 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 87
Alice has generated random secret data bits, a:  [0 1 0 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 0 1 1]
Bob has chosen random basis, b':  [1 1 1 0 0 1 1 1]
Eve has chosen random basis:  [1 1 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [1 1 1 0 0 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 88
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 0 1 0]
Bob has chosen random basis, b':  [0 1 1 1 1 1 0 0]
Eve has chosen random basis:  [0 1 1 1 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 89
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 0 1 0]
Bob has chosen random basis, b':  [0 1 1 1 1 1 0 0]
Eve has chosen random basis:  [1 1 1 1 1 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 1 0 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 90
Alice has generated random secret data bits, a:  [0 0 0 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 1 1 0 0]
Bob has chosen random basis, b':  [1 1 0 1 0 0 1 1]
Eve has chosen random basis:  [1 0 1 0 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Simulation round: 91
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 0 0 0]
Bob has chosen random basis, b':  [0 1 1 1 0 0 1 0]
Eve has chosen random basis:  [0 0 0 0 1 1 1 1]
Simulating...
Bob's measurement result:  [0 0 0 0 0 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 92
Alice has generated random secret data bits, a:  [1 0 0 1 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 0 1 1]
Bob has chosen random basis, b':  [0 1 0 1 0 0 0 0]
Eve has chosen random basis:  [0 0 1 1 0 0 1 1]
Simulating...
Bob's measurement result:  [1 1 0 0 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 1]
Simulation round: 93
Alice has generated random secret data bits, a:  [0 0 0 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 0 0 1]
Bob has chosen random basis, b':  [1 0 0 1 0 0 1 0]
Eve has chosen random basis:  [0 1 1 0 1 1 0 0]
Simulating...
Bob's measurement result:  [0 0 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [0]
Interference detected... Aborting!
Simulation round: 94
Alice has generated random secret data bits, a:  [1 0 0 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 1 0 0]
Bob has chosen random basis, b':  [1 0 0 1 0 0 0 1]
Eve has chosen random basis:  [1 1 1 1 1 0 1 1]
Simulating...
Bob's measurement result:  [1 0 0 1 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Simulation round: 95
Alice has generated random secret data bits, a:  [0 0 1 1 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 1 0 1 0]
Bob has chosen random basis, b':  [0 1 1 1 0 0 1 1]
Eve has chosen random basis:  [1 0 0 0 0 0 0 1]
Simulating...
Bob's measurement result:  [1 0 1 1 0 1 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Simulation round: 96
Alice has generated random secret data bits, a:  [1 1 1 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 0 1 0 0]
Bob has chosen random basis, b':  [1 0 0 1 1 0 1 0]
Eve has chosen random basis:  [1 1 1 1 0 1 0 0]
Simulating...
Bob's measurement result:  [1 0 1 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 97
Alice has generated random secret data bits, a:  [1 1 0 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 0 1 1]
Bob has chosen random basis, b':  [0 0 0 0 0 1 1 0]
Eve has chosen random basis:  [0 1 0 1 0 0 1 1]
Simulating...
Bob's measurement result:  [1 1 0 1 1 0 0 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 98
Alice has generated random secret data bits, a:  [0 0 1 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 0 1 1]
Bob has chosen random basis, b':  [0 1 1 1 0 1 1 1]
Eve has chosen random basis:  [1 0 1 0 1 1 1 1]
Simulating...
Bob's measurement result:  [0 0 1 1 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 99
Alice has generated random secret data bits, a:  [1 0 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 0 0 1 0]
Bob has chosen random basis, b':  [0 1 1 1 1 1 1 1]
Eve has chosen random basis:  [1 0 1 1 1 0 1 0]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 100
Alice has generated random secret data bits, a:  [1 0 0 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 0 0 1]
Bob has chosen random basis, b':  [0 1 0 1 0 1 1 1]
Eve has chosen random basis:  [1 1 0 1 0 1 1 1]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Simulation round: 101
Alice has generated random secret data bits, a:  [0 1 1 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 0 1 1]
Bob has chosen random basis, b':  [0 0 0 0 0 1 0 0]
Eve has chosen random basis:  [1 1 0 1 1 0 0 0]
Simulating...
Bob's measurement result:  [1 0 0 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 102
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 0 0 1]
Bob has chosen random basis, b':  [0 1 0 0 0 1 1 0]
Eve has chosen random basis:  [0 0 1 0 0 0 0 0]
Simulating...
Bob's measurement result:  [1 1 0 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 0]
Simulation round: 103
Alice has generated random secret data bits, a:  [1 0 1 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 1 1 1]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 0]
Eve has chosen random basis:  [0 0 1 0 0 0 1 0]
Simulating...
Bob's measurement result:  [1 0 1 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Simulation round: 104
Alice has generated random secret data bits, a:  [0 1 0 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 0 1 0]
Bob has chosen random basis, b':  [1 1 1 1 1 1 1 1]
Eve has chosen random basis:  [0 0 1 0 0 1 0 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Simulation round: 105
Alice has generated random secret data bits, a:  [0 1 1 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 0 1 0]
Bob has chosen random basis, b':  [1 1 1 1 0 0 1 1]
Eve has chosen random basis:  [1 0 1 1 1 0 0 0]
Simulating...
Bob's measurement result:  [0 0 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 1 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [0 1]
Simulation round: 106
Alice has generated random secret data bits, a:  [0 0 0 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 1 0 1]
Bob has chosen random basis, b':  [0 1 1 0 0 1 1 0]
Eve has chosen random basis:  [1 1 1 0 0 0 1 1]
Simulating...
Bob's measurement result:  [0 0 0 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 107
Alice has generated random secret data bits, a:  [0 1 0 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 1 0 0 0]
Bob has chosen random basis, b':  [1 1 1 0 0 1 1 1]
Eve has chosen random basis:  [1 1 1 1 0 0 1 0]
Simulating...
Bob's measurement result:  [0 1 0 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Simulation round: 108
Alice has generated random secret data bits, a:  [1 0 0 0 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 1 1]
Bob has chosen random basis, b':  [1 0 0 0 0 1 1 0]
Eve has chosen random basis:  [0 0 1 0 1 1 0 0]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 109
Alice has generated random secret data bits, a:  [0 0 0 1 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 0 0 0]
Bob has chosen random basis, b':  [1 1 0 0 0 0 1 0]
Eve has chosen random basis:  [1 1 0 1 0 0 0 1]
Simulating...
Bob's measurement result:  [0 0 0 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 0 0 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Simulation round: 110
Alice has generated random secret data bits, a:  [1 0 1 0 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 1 1 0]
Bob has chosen random basis, b':  [0 0 1 1 0 1 1 1]
Eve has chosen random basis:  [1 0 1 0 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 0]
Interference detected... Aborting!
Simulation round: 111
Alice has generated random secret data bits, a:  [0 1 0 1 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 0 1 0 0]
Bob has chosen random basis, b':  [0 0 0 1 0 1 1 1]
Eve has chosen random basis:  [0 0 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 0 0 1 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [1 0]
Simulation round: 112
Alice has generated random secret data bits, a:  [0 0 1 0 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 1 1 0]
Bob has chosen random basis, b':  [1 1 1 0 1 0 1 1]
Eve has chosen random basis:  [0 0 1 1 1 1 1 1]
Simulating...
Bob's measurement result:  [0 0 1 0 0 1 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Simulation round: 113
Alice has generated random secret data bits, a:  [0 0 1 0 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 1 0 0 1]
Bob has chosen random basis, b':  [1 1 0 1 1 1 0 0]
Eve has chosen random basis:  [0 0 1 0 1 1 0 1]
Simulating...
Bob's measurement result:  [0 0 1 0 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 0]
Simulation round: 114
Alice has generated random secret data bits, a:  [0 1 1 0 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 0 1 0]
Bob has chosen random basis, b':  [1 0 1 1 1 1 0 1]
Eve has chosen random basis:  [1 0 0 0 0 1 0 0]
Simulating...
Bob's measurement result:  [0 1 0 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 1 1 0]
Key Exchange without eavesdropping: 
Aborting protocol. Less than 2n bits match between b and b'
Key Exchange with eavesdropping: 
Aborting protocol. Less than 2n bits match between b and b'
Simulation round: 115
Alice has generated random secret data bits, a:  [1 1 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 0 1 0]
Bob has chosen random basis, b':  [1 0 1 0 0 1 1 1]
Eve has chosen random basis:  [0 0 1 0 0 0 1 0]
Simulating...
Bob's measurement result:  [1 1 0 0 0 1 0 0]
Bob's measurement result with eavesdropping:  [1 1 0 0 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Interference detected... Aborting!
Simulation round: 116
Alice has generated random secret data bits, a:  [0 1 0 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 1 0 0]
Bob has chosen random basis, b':  [0 1 0 0 0 0 0 1]
Eve has chosen random basis:  [0 0 0 1 1 1 0 0]
Simulating...
Bob's measurement result:  [0 1 1 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 0]
Simulation round: 117
Alice has generated random secret data bits, a:  [0 0 0 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 1 1 0]
Bob has chosen random basis, b':  [1 0 0 0 0 1 0 0]
Eve has chosen random basis:  [0 0 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 0 0 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Simulation round: 118
Alice has generated random secret data bits, a:  [0 1 0 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 1 1 0]
Bob has chosen random basis, b':  [0 1 0 0 0 1 0 0]
Eve has chosen random basis:  [0 1 0 1 0 0 1 1]
Simulating...
Bob's measurement result:  [0 0 0 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [0 1]
Simulation round: 119
Alice has generated random secret data bits, a:  [1 0 0 1 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 0 0 0]
Bob has chosen random basis, b':  [1 0 1 1 1 1 0 1]
Eve has chosen random basis:  [1 1 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [1 0 0 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Successfully exchanged private key:  [0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1]
Bob has check bits:  [0 1]
Interference detected... Aborting!
Simulation round: 120
Alice has generated random secret data bits, a:  [0 0 0 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 0 1 1]
Bob has chosen random basis, b':  [0 0 1 0 0 1 1 1]
Eve has chosen random basis:  [0 1 0 0 0 1 0 0]
Simulating...
Bob's measurement result:  [0 0 0 1 1 1 1 1]
Bob's measurement result with eavesdropping:  [0 0 0 1 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 1]
Simulation round: 121
Alice has generated random secret data bits, a:  [0 1 0 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 0 1 0 1]
Bob has chosen random basis, b':  [1 0 0 1 0 1 1 1]
Eve has chosen random basis:  [0 1 1 0 0 0 0 0]
Simulating...
Bob's measurement result:  [1 0 0 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0]
Bob has check bits:  [0 0]
Successfully exchanged private key:  [1 0]
Simulation round: 122
Alice has generated random secret data bits, a:  [0 1 0 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 1 0 1]
Bob has chosen random basis, b':  [0 0 1 0 1 1 0 1]
Eve has chosen random basis:  [1 1 1 0 0 0 1 1]
Simulating...
Bob's measurement result:  [1 1 1 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 123
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 0 0]
Bob has chosen random basis, b':  [0 0 0 0 0 0 1 0]
Eve has chosen random basis:  [0 1 1 0 0 1 0 1]
Simulating...
Bob's measurement result:  [1 1 0 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 1]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 124
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 1 1 1 0]
Bob has chosen random basis, b':  [1 0 0 1 0 0 0 1]
Eve has chosen random basis:  [0 1 1 1 1 1 0 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0]
Bob has check bits:  [0]
Successfully exchanged private key:  [0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0]
Bob has check bits:  [0]
Successfully exchanged private key:  [0]
Simulation round: 125
Alice has generated random secret data bits, a:  [1 1 0 1 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 1 0 0]
Bob has chosen random basis, b':  [1 1 0 0 0 1 0 0]
Eve has chosen random basis:  [0 1 1 0 0 1 0 1]
Simulating...
Bob's measurement result:  [1 1 0 1 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Interference detected... Aborting!
Simulation round: 126
Alice has generated random secret data bits, a:  [1 1 0 1 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 1 0 1]
Bob has chosen random basis, b':  [1 0 1 1 0 1 1 0]
Eve has chosen random basis:  [0 0 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0]
Bob has check bits:  [1 0]
Successfully exchanged private key:  [1 0]
Simulation round: 127
Alice has generated random secret data bits, a:  [0 0 1 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 0 0 1 0]
Bob has chosen random basis, b':  [1 0 1 0 1 1 0 1]
Eve has chosen random basis:  [0 0 1 0 1 1 0 1]
Simulating...
Bob's measurement result:  [1 1 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1]
Bob has check bits:  [1]
Successfully exchanged private key:  [1]
n= 2
Successful key exchanges without Eve present:  127
Successful key exchanges with Eve present:  66
Simulation round: 0
Alice has generated random secret data bits, a:  [1 1 0 0 0 1 1 0 1 0 1 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 1 1 0 1 0 1 1 1 0 0]
Bob has chosen random basis, b':  [0 0 1 1 0 1 1 1 1 0 1 0 1 0 0 0]
Eve has chosen random basis:  [0 1 0 1 1 1 1 0 1 1 1 1 0 1 0 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 1 0 0 1 0 0 0 0 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [0 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 1
Alice has generated random secret data bits, a:  [0 0 0 1 1 0 1 1 1 1 0 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 1 1 1 0 1 0 0 0 0 1 1]
Bob has chosen random basis, b':  [0 1 1 0 1 0 0 1 1 1 0 0 1 0 1 1]
Eve has chosen random basis:  [0 1 1 1 0 0 0 0 1 1 0 1 0 1 1 0]
Simulating...
Bob's measurement result:  [1 0 0 1 0 0 0 1 0 1 0 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 1 1 1 1 1 0 1 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 2
Alice has generated random secret data bits, a:  [0 1 0 1 1 1 0 1 0 1 1 0 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 1 0 0 1 1 1 0 0 1 0 1]
Bob has chosen random basis, b':  [1 1 1 1 1 0 1 0 0 1 0 1 1 0 0 0]
Eve has chosen random basis:  [1 1 0 1 0 0 1 1 0 0 0 1 1 1 0 1]
Simulating...
Bob's measurement result:  [0 1 0 1 1 0 0 1 1 1 1 1 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 0 1 1 0 0 0 1 1 1 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 0 0 1]
Interference detected... Aborting!
Simulation round: 3
Alice has generated random secret data bits, a:  [0 1 1 1 1 1 0 1 0 0 1 0 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 0 1 1 1 1 1 1 1 1 1 0 1]
Bob has chosen random basis, b':  [0 0 0 1 0 0 0 0 0 1 0 1 0 0 1 0]
Eve has chosen random basis:  [0 0 1 0 1 1 0 0 0 1 1 1 0 0 0 1]
Simulating...
Bob's measurement result:  [0 1 1 1 1 1 0 0 1 0 1 0 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 0 1 0 1 1 0 1 0 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 0 1 0]
Interference detected... Aborting!
Simulation round: 4
Alice has generated random secret data bits, a:  [1 1 0 0 0 1 0 0 0 0 1 1 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0]
Bob has chosen random basis, b':  [1 1 0 1 0 0 1 0 1 1 1 0 0 1 0 0]
Eve has chosen random basis:  [1 1 0 1 0 0 0 0 0 1 0 0 0 1 1 0]
Simulating...
Bob's measurement result:  [1 1 0 0 0 1 1 0 0 0 1 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 0 1 0 0 0 1 1 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 1 0 1]
Successfully exchanged private key:  [0 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 5
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 0 0 0 1 1 1 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 1 0 1 1 1 0 0 1 1 1 1]
Bob has chosen random basis, b':  [0 1 1 1 1 1 0 0 1 0 0 0 0 1 0 1]
Eve has chosen random basis:  [1 0 1 1 1 0 1 0 1 0 0 1 0 0 0 0]
Simulating...
Bob's measurement result:  [0 1 0 0 1 1 0 0 0 0 1 1 0 0 0 0]
Bob's measurement result with eavesdropping:  [1 1 0 0 1 1 1 1 0 1 1 0 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Interference detected... Aborting!
Simulation round: 6
Alice has generated random secret data bits, a:  [0 0 0 0 0 0 1 1 1 0 0 1 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 1 1 0 0 1 0 0 0 0 0 1]
Bob has chosen random basis, b':  [0 1 0 0 0 0 0 0 0 0 1 1 1 0 1 0]
Eve has chosen random basis:  [1 0 0 0 1 0 1 1 1 0 0 1 1 1 0 1]
Simulating...
Bob's measurement result:  [0 0 1 0 1 1 0 1 1 0 0 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 1 1 1 0 1 0 1 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [0 0 0 1]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 7
Alice has generated random secret data bits, a:  [1 0 0 1 1 0 1 1 0 0 1 1 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 1 0 0 1 0 1 1 0 0 0 1]
Bob has chosen random basis, b':  [1 0 1 1 1 0 1 1 1 1 1 0 1 0 1 1]
Eve has chosen random basis:  [0 1 1 0 0 0 1 1 1 1 1 0 1 0 0 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 0 0 1 0 0 1 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 1 1 1 1 0 0 1 0 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [1 1 0 1]
Successfully exchanged private key:  [0 1 0 0]
Simulation round: 8
Alice has generated random secret data bits, a:  [1 1 1 0 0 1 0 0 1 0 0 1 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 0 0 0 1 1 1 1 1 0 0 0]
Bob has chosen random basis, b':  [1 0 0 0 1 0 0 1 1 1 1 1 1 1 1 0]
Eve has chosen random basis:  [0 1 1 1 0 1 0 1 0 1 0 1 0 0 0 0]
Simulating...
Bob's measurement result:  [1 1 1 0 0 1 0 1 1 0 0 1 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 0 1 1 0 0 1 1 0 0 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [0 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 0 1]
Interference detected... Aborting!
Simulation round: 9
Alice has generated random secret data bits, a:  [1 1 1 0 0 0 0 0 1 0 1 0 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 0 1 0 0 1 0 1 1 0 0]
Bob has chosen random basis, b':  [0 0 0 1 0 0 0 1 1 0 0 0 0 0 0 0]
Eve has chosen random basis:  [1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 1]
Simulating...
Bob's measurement result:  [1 1 1 1 0 0 0 0 0 0 1 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 0 0 0 1 0 1 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 10
Alice has generated random secret data bits, a:  [0 1 1 1 1 1 1 0 0 1 1 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 0 0 1 1 0 1 1 1 0 1 0]
Bob has chosen random basis, b':  [1 1 1 1 1 0 0 0 1 0 0 1 1 0 1 0]
Eve has chosen random basis:  [1 0 1 0 0 1 1 0 1 0 1 1 1 1 1 1]
Simulating...
Bob's measurement result:  [0 1 1 1 1 1 1 1 0 1 0 1 0 0 1 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 0 1 1 0 1 1 0 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [0 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 0 1]
Interference detected... Aborting!
Simulation round: 11
Alice has generated random secret data bits, a:  [1 0 1 1 1 1 1 0 1 0 1 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 0 1 1 1 0 1 1 1 1 0 1]
Bob has chosen random basis, b':  [0 0 1 0 0 0 0 0 0 1 1 1 0 0 0 0]
Eve has chosen random basis:  [0 1 1 0 1 1 0 0 1 1 0 1 1 1 1 1]
Simulating...
Bob's measurement result:  [0 0 1 1 0 1 0 0 0 1 1 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 0 0 1 1 0 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [1 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 0 1 0]
Interference detected... Aborting!
Simulation round: 12
Alice has generated random secret data bits, a:  [0 0 1 1 0 1 0 0 1 1 0 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 1 0 1 1 1 1 0 1 1 1 0 1]
Bob has chosen random basis, b':  [1 1 1 0 1 1 0 1 1 0 0 1 0 0 0 0]
Eve has chosen random basis:  [1 0 1 1 0 1 1 1 0 0 0 0 1 1 1 1]
Simulating...
Bob's measurement result:  [0 0 1 0 0 0 1 0 1 0 0 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 1 0 0 1 0 0 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [1 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [1 0 0 0]
Interference detected... Aborting!
Simulation round: 13
Alice has generated random secret data bits, a:  [1 1 1 1 1 1 1 1 0 0 0 0 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 1 0 1 1 0 0 0 0 0 0 1]
Bob has chosen random basis, b':  [1 0 1 0 0 1 1 0 1 1 1 0 1 0 1 1]
Eve has chosen random basis:  [0 0 1 0 0 1 1 0 1 1 0 0 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 0 1 1 1 0 1 0 1 0 0 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 1 1 1 1 0 0 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 14
Alice has generated random secret data bits, a:  [0 1 1 0 1 0 1 0 1 0 1 1 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 0 0 1 1 0 1 1 1 1 1 0]
Bob has chosen random basis, b':  [1 1 1 0 1 0 0 0 1 1 1 1 1 1 0 0]
Eve has chosen random basis:  [1 0 0 1 1 1 1 0 1 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 1 1 0 0 0 1 0 1 0 1 1 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 1 0 0 0 0 1 1 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 15
Alice has generated random secret data bits, a:  [0 0 0 1 1 0 0 1 1 0 0 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 0 0 1 0 0 0 0 0 0 1 1]
Bob has chosen random basis, b':  [0 0 1 1 1 1 0 0 1 1 0 1 0 1 1 0]
Eve has chosen random basis:  [1 0 0 1 0 1 0 1 1 0 0 0 1 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 1 1 1 0 0 0 1 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 1 0 0 1 1 1 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 0 1 0]
Interference detected... Aborting!
Simulation round: 16
Alice has generated random secret data bits, a:  [0 1 1 0 1 1 0 1 0 1 0 1 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 0 1 1 0 1 0 1 0 0 1 0]
Bob has chosen random basis, b':  [1 1 1 1 0 1 0 1 0 1 1 0 1 0 1 1]
Eve has chosen random basis:  [0 1 0 0 1 1 0 0 1 1 0 0 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 0 0 0 1 0 1 1 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 1 1 1 1 0 1 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 1 0 0]
Interference detected... Aborting!
Simulation round: 17
Alice has generated random secret data bits, a:  [0 1 0 1 1 0 0 0 0 0 0 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 1 0 0 1 0 0 1 0 0 1 0]
Bob has chosen random basis, b':  [1 0 1 1 1 0 0 1 1 0 0 1 0 1 1 1]
Eve has chosen random basis:  [1 1 0 0 1 1 1 1 0 0 0 1 1 0 1 1]
Simulating...
Bob's measurement result:  [1 1 0 1 1 0 0 0 0 0 0 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 0 1 0 0 0 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 18
Alice has generated random secret data bits, a:  [0 0 0 0 0 1 0 0 0 1 1 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 1 0 1 0 1 0 0 1 0 1 1]
Bob has chosen random basis, b':  [0 1 1 1 0 0 1 0 0 1 1 0 0 1 0 0]
Eve has chosen random basis:  [0 0 1 0 1 0 1 1 0 0 1 1 1 0 0 0]
Simulating...
Bob's measurement result:  [0 1 1 1 1 1 1 0 0 1 0 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 1 0 0 0 1 1 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [0 0 1 0]
Simulation round: 19
Alice has generated random secret data bits, a:  [0 0 0 1 1 0 1 0 0 0 1 0 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 1 0 1 1 0 0 1 1 1 0 1]
Bob has chosen random basis, b':  [1 0 0 0 0 1 1 0 1 1 0 1 1 0 0 1]
Eve has chosen random basis:  [0 1 1 1 1 1 1 0 0 0 1 0 0 0 0 0]
Simulating...
Bob's measurement result:  [0 0 0 1 1 0 0 1 0 1 1 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 0 1 0 0 0 1 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 1 0 0]
Successfully exchanged private key:  [0 1 1 0]
Simulation round: 20
Alice has generated random secret data bits, a:  [1 1 1 1 0 1 1 1 1 0 0 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 1 1 1 1 0 0 0 0 0 1 1]
Bob has chosen random basis, b':  [1 1 1 0 0 0 1 0 1 1 0 0 0 1 1 1]
Eve has chosen random basis:  [0 1 0 0 1 0 1 1 1 1 0 1 1 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 0 0 1 0 0 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [0 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 21
Alice has generated random secret data bits, a:  [0 0 0 0 0 0 1 0 1 1 0 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 0 0 1 0 1 0 1 0 0 0 1 0]
Bob has chosen random basis, b':  [1 1 1 1 0 1 1 1 1 0 0 1 0 0 1 1]
Eve has chosen random basis:  [0 0 0 0 1 0 1 0 0 1 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 0 1 1 0 1 0 1 0 1 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [0 0 0 1]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [0 0 1 1]
Interference detected... Aborting!
Simulation round: 22
Alice has generated random secret data bits, a:  [0 1 1 1 1 1 1 1 0 0 1 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 0]
Bob has chosen random basis, b':  [0 0 1 1 0 0 1 0 0 0 0 1 0 1 1 0]
Eve has chosen random basis:  [0 0 0 1 1 1 0 0 0 0 0 1 0 1 1 0]
Simulating...
Bob's measurement result:  [1 1 1 1 0 1 1 1 1 0 1 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 1 0 0 0 0 1 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 23
Alice has generated random secret data bits, a:  [0 1 1 1 1 1 0 1 0 0 0 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 0 0 0 1 0 0 1 1 0 1 1]
Bob has chosen random basis, b':  [1 0 1 0 1 1 1 1 0 0 0 1 1 0 1 0]
Eve has chosen random basis:  [0 1 0 0 1 1 0 1 1 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 1 0 1 1 0 1 0 0 0 0 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 1 1 1 0 1 0 0 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 0 1]
Interference detected... Aborting!
Simulation round: 24
Alice has generated random secret data bits, a:  [0 1 1 0 0 0 1 0 1 0 0 0 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 1 1 1 1 1 1 1 0 0 1 0]
Bob has chosen random basis, b':  [0 0 1 1 1 0 0 0 1 1 1 0 0 1 1 0]
Eve has chosen random basis:  [1 1 1 1 1 0 1 1 1 0 1 0 0 1 0 1]
Simulating...
Bob's measurement result:  [0 1 0 1 0 0 0 1 1 0 0 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 1 1 0 0 0 1 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 0 0 0]
Interference detected... Aborting!
Simulation round: 25
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 1 0 0 0 1 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 0 1 1 1 1 0 1 0 0 0 1]
Bob has chosen random basis, b':  [0 0 0 1 1 0 0 1 1 1 0 1 1 0 1 0]
Eve has chosen random basis:  [0 1 0 0 1 0 1 0 1 0 1 1 0 0 0 1]
Simulating...
Bob's measurement result:  [0 1 0 1 0 0 0 0 0 0 1 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 0 0 0 1 0 1 0 1 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [0 1 0 0]
Simulation round: 26
Alice has generated random secret data bits, a:  [1 0 0 0 1 1 1 1 1 1 1 1 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 1 1 0 1 0 0 0 0 1 0 1]
Bob has chosen random basis, b':  [0 1 1 0 1 0 0 0 1 0 1 0 1 0 1 1]
Eve has chosen random basis:  [0 1 1 0 1 0 0 1 1 1 1 0 0 1 1 0]
Simulating...
Bob's measurement result:  [1 0 1 0 0 0 1 1 1 1 0 1 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 0 0 1 0 0 1 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [1 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 0 0]
Interference detected... Aborting!
Simulation round: 27
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 1 0 0 0 0 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 1 1 0 1 0 0 1 1 0 1 0]
Bob has chosen random basis, b':  [0 0 1 0 0 0 1 0 0 1 1 1 1 1 1 1]
Eve has chosen random basis:  [1 0 0 0 1 1 0 0 0 0 1 0 0 0 1 1]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 1 0 0 0 0 1 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 0 1 0 0 0 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [0 0 1 0]
Interference detected... Aborting!
Simulation round: 28
Alice has generated random secret data bits, a:  [1 1 0 0 1 1 0 0 0 0 0 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 0 0 0 0 0 1 1 1 1 1 1]
Bob has chosen random basis, b':  [1 0 1 1 1 0 1 1 1 1 1 1 0 0 1 1]
Eve has chosen random basis:  [1 1 1 0 1 1 1 0 1 1 1 0 1 0 0 0]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 1 0 0 1 0 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 0 0 0 0 0 1 1 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 1 0 1]
Interference detected... Aborting!
Simulation round: 29
Alice has generated random secret data bits, a:  [0 1 1 0 1 0 1 0 0 1 1 0 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 1 0 1 0 1 0 0 0 1 1 1]
Bob has chosen random basis, b':  [0 1 0 0 1 0 1 1 0 0 1 0 1 0 0 0]
Eve has chosen random basis:  [0 1 1 1 1 0 0 1 1 1 0 1 0 0 0 0]
Simulating...
Bob's measurement result:  [0 1 1 0 1 1 1 0 0 1 1 0 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 1 0 0 0 0 1 1 0 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [1 0 0 0]
Simulation round: 30
Alice has generated random secret data bits, a:  [0 0 1 0 1 1 1 0 1 0 1 1 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 1 0 0 0 0 0 1 1 0 1 0]
Bob has chosen random basis, b':  [0 0 1 0 1 0 0 0 0 1 1 1 1 1 1 1]
Eve has chosen random basis:  [1 0 1 1 1 0 0 1 0 1 1 0 0 1 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 0 1 0 1 1 0 1 0 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 1 1 0 1 0 1 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 0 1 0]
Interference detected... Aborting!
Simulation round: 31
Alice has generated random secret data bits, a:  [1 0 0 0 0 0 1 0 1 0 0 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 0 1 0 0 1 0 1 1 0 1]
Bob has chosen random basis, b':  [0 1 0 1 0 0 0 0 1 0 0 1 0 0 1 0]
Eve has chosen random basis:  [1 0 1 1 1 0 1 0 1 1 0 0 1 1 0 1]
Simulating...
Bob's measurement result:  [1 0 0 1 0 0 1 0 1 0 1 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 0 0 1 1 0 0 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [1 0 0 0]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 32
Alice has generated random secret data bits, a:  [0 1 0 1 0 1 1 0 1 0 0 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 1 0 0 0 0 0 1 0 0 0 0]
Bob has chosen random basis, b':  [1 1 1 0 0 1 1 0 1 1 0 0 1 0 1 0]
Eve has chosen random basis:  [1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1]
Simulating...
Bob's measurement result:  [1 1 0 1 1 1 1 0 0 0 0 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 1 1 1 0 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 33
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0]
Bob has chosen random basis, b':  [0 0 1 0 0 0 1 1 1 1 0 0 1 1 0 1]
Eve has chosen random basis:  [1 0 1 1 1 0 0 0 0 1 0 0 0 0 0 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 1 1 1 1 0 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 1 1 0 0 1 0 0 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 0 0]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 34
Alice has generated random secret data bits, a:  [1 1 1 0 0 1 0 1 0 1 0 1 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 0 1 1 0 1 0 0 0 1 1 1]
Bob has chosen random basis, b':  [1 1 1 0 0 1 0 1 1 1 0 0 0 1 0 1]
Eve has chosen random basis:  [0 0 0 1 0 0 1 0 1 0 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 1 1 1 1 1 0 1 0 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 0 1 0 0 1 0 1 0 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [1 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 35
Alice has generated random secret data bits, a:  [0 0 0 1 0 0 1 0 1 1 0 1 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 1 0 1 0 0 1 1 0 1 1 1]
Bob has chosen random basis, b':  [0 0 0 1 0 1 1 1 0 0 1 0 1 1 0 0]
Eve has chosen random basis:  [0 1 1 0 0 1 1 1 1 0 1 0 0 0 0 0]
Simulating...
Bob's measurement result:  [0 0 0 1 0 0 0 0 1 1 0 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 1 1 0 1 1 1 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [1 0 1 0]
Interference detected... Aborting!
Simulation round: 36
Alice has generated random secret data bits, a:  [1 1 1 1 1 1 0 0 0 0 1 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 0 0 1 0 0 1 0 0 0 0]
Bob has chosen random basis, b':  [1 0 1 0 1 1 1 1 1 0 0 1 1 1 1 1]
Eve has chosen random basis:  [0 0 0 1 0 0 1 0 1 0 1 1 0 1 1 1]
Simulating...
Bob's measurement result:  [1 1 1 1 1 1 0 1 0 0 1 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 0 1 0 0 0 0 0 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [0 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 37
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 1 1 0 0 0 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 0 0 1 0 1 0 0 1 1 1 1]
Bob has chosen random basis, b':  [1 0 1 1 0 0 1 0 0 1 1 1 1 0 0 0]
Eve has chosen random basis:  [1 0 1 1 0 0 1 1 1 1 0 0 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 0 1 0 0 0 0 0 0 1 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 0 1 1 0 1 1 1 0 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 38
Alice has generated random secret data bits, a:  [0 1 0 0 1 1 1 0 0 0 1 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 0 1 1 0 1 1 1 0 1 1 0]
Bob has chosen random basis, b':  [0 0 0 0 1 0 1 1 1 1 0 0 0 1 0 1]
Eve has chosen random basis:  [0 0 1 0 1 0 1 0 1 0 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 1 0 0 0 0 1 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 0 0 0 0 0 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 0]
Interference detected... Aborting!
Simulation round: 39
Alice has generated random secret data bits, a:  [1 0 1 1 0 1 0 1 0 0 0 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 0 1 0 0 0 1 1 1 1 0 0]
Bob has chosen random basis, b':  [0 0 1 0 1 1 1 0 0 0 1 0 0 1 1 0]
Eve has chosen random basis:  [1 1 1 0 0 0 1 0 1 0 0 1 1 0 1 1]
Simulating...
Bob's measurement result:  [1 0 1 1 0 1 0 1 0 0 0 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 0 1 1 0 0 0 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [0 1 0 1]
Interference detected... Aborting!
Simulation round: 40
Alice has generated random secret data bits, a:  [1 1 1 0 0 1 0 0 1 0 1 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 1 1 1 0 1 1 0 1 1 1]
Bob has chosen random basis, b':  [1 1 1 1 0 1 0 0 1 1 0 1 0 1 1 1]
Eve has chosen random basis:  [1 1 1 0 0 0 0 0 0 0 1 0 0 0 0 1]
Simulating...
Bob's measurement result:  [1 1 1 1 0 1 1 0 1 0 1 0 0 1 0 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 0 1 1 1 1 0 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 1 0 1]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 41
Alice has generated random secret data bits, a:  [0 0 1 0 0 1 0 1 0 0 0 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 0 0 1 1 1 1 0 1 0 1 0]
Bob has chosen random basis, b':  [1 1 0 1 1 1 1 0 1 1 1 1 1 0 0 0]
Eve has chosen random basis:  [1 1 1 1 1 0 1 0 1 0 0 1 1 0 1 1]
Simulating...
Bob's measurement result:  [1 0 1 0 0 0 0 0 0 0 0 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 1 0 1 1 0 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [1 0 0 0]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [0 1 1 0]
Interference detected... Aborting!
Simulation round: 42
Alice has generated random secret data bits, a:  [1 1 0 1 1 1 1 0 1 0 0 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 1 1 1 1 0 0 0 0 1 1 1]
Bob has chosen random basis, b':  [1 0 0 0 0 1 0 0 1 1 1 0 0 1 1 0]
Eve has chosen random basis:  [0 1 0 0 1 1 1 0 1 1 1 0 0 0 1 1]
Simulating...
Bob's measurement result:  [0 0 0 1 1 1 0 0 1 1 0 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 1 0 0 0 0 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [0 1 0 0]
Simulation round: 43
Alice has generated random secret data bits, a:  [1 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 0 0 1 1 0 1 0 1 1 0 1]
Bob has chosen random basis, b':  [1 1 1 0 1 0 1 0 1 0 1 1 1 1 0 1]
Eve has chosen random basis:  [1 0 1 1 0 1 1 1 0 1 0 1 0 0 0 0]
Simulating...
Bob's measurement result:  [1 1 0 0 1 0 1 1 0 0 0 1 0 0 0 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 0 0 0 0 0 0 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [1 0 0 0]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [0 0 0 0]
Simulation round: 44
Alice has generated random secret data bits, a:  [1 0 1 0 0 1 0 0 0 1 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 1 0 0 1 1 1 1 1 1 1 1]
Bob has chosen random basis, b':  [1 0 1 0 0 1 1 1 1 1 1 0 1 1 0 1]
Eve has chosen random basis:  [1 0 0 1 0 1 1 0 1 1 1 0 1 0 1 0]
Simulating...
Bob's measurement result:  [1 0 1 0 0 1 0 0 0 1 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 1 0 1 0 0 0 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Interference detected... Aborting!
Simulation round: 45
Alice has generated random secret data bits, a:  [1 1 1 0 0 1 0 1 0 0 0 1 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 0 0 1 0 0 0 1 0 1 1 1]
Bob has chosen random basis, b':  [0 1 1 0 1 0 0 1 0 1 0 0 1 1 0 1]
Eve has chosen random basis:  [1 0 0 1 1 0 1 1 0 0 1 1 1 0 1 0]
Simulating...
Bob's measurement result:  [1 1 0 1 0 1 0 1 0 1 0 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 0 1 1 0 0 0 0 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [0 0 0 0]
Simulation round: 46
Alice has generated random secret data bits, a:  [0 1 1 0 0 1 1 1 0 1 1 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 0 1 0 0 0 0 1 1 1 1 0]
Bob has chosen random basis, b':  [1 1 1 0 0 0 0 1 1 0 0 1 1 0 1 1]
Eve has chosen random basis:  [0 1 0 0 0 1 1 1 1 1 0 1 1 0 0 1]
Simulating...
Bob's measurement result:  [1 1 1 0 0 1 0 1 1 1 1 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 1 0 0 1 1 1 0 1 1 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [1 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 47
Alice has generated random secret data bits, a:  [1 0 0 0 1 0 0 1 1 0 0 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 1 1 1 1 0 1 1 0 0 0 0]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 1 1 1 0 1 0 1 0 0]
Eve has chosen random basis:  [0 0 0 1 0 0 0 0 0 1 1 0 1 1 0 0]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 0 1 1 1 0 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 0 0 1 1 0 0 0 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 48
Alice has generated random secret data bits, a:  [1 0 1 0 1 0 1 1 1 1 1 1 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 1 0 0 0 1 1 0 1 0 0 1]
Bob has chosen random basis, b':  [1 1 1 0 0 1 0 1 1 1 1 0 1 0 1 1]
Eve has chosen random basis:  [1 1 1 1 1 0 0 0 1 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 0 1 0 1 1 1 1 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 0 1 1 1 1 1 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 0 1 1]
Simulation round: 49
Alice has generated random secret data bits, a:  [1 0 0 1 0 0 1 0 0 1 0 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 0 1 0 1 1 1 0 1 0 0 0]
Bob has chosen random basis, b':  [1 0 1 0 0 0 0 0 0 1 1 1 0 1 1 0]
Eve has chosen random basis:  [0 1 1 0 0 0 0 0 0 1 1 1 1 0 1 0]
Simulating...
Bob's measurement result:  [1 0 0 1 1 0 0 0 0 1 0 0 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 0 0 1 0 1 1 1 1 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [1 0 0 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 0]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 50
Alice has generated random secret data bits, a:  [1 0 0 1 0 0 1 1 0 1 0 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 1 1 0 1 0 1 1 0 1 1 1]
Bob has chosen random basis, b':  [1 1 0 1 1 0 0 1 0 1 1 1 0 1 1 0]
Eve has chosen random basis:  [1 1 0 0 0 1 1 1 1 0 0 0 1 0 0 0]
Simulating...
Bob's measurement result:  [1 1 0 1 0 0 1 1 0 1 0 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 0 1 1 0 0 0 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Interference detected... Aborting!
Simulation round: 51
Alice has generated random secret data bits, a:  [0 1 1 0 0 1 1 0 0 0 0 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 1 1 0 1 1 0 1 1 1 1 1]
Bob has chosen random basis, b':  [1 0 1 1 1 1 1 1 1 1 0 1 0 1 1 0]
Eve has chosen random basis:  [0 0 1 0 0 0 0 1 0 1 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [1 1 1 0 0 1 1 1 0 0 0 0 0 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 1 1 0 0 1 0 0 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 1 0 1]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 52
Alice has generated random secret data bits, a:  [0 0 0 0 1 0 1 1 0 0 0 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 0 0 0 1 1 1 0 1 0 0 1]
Bob has chosen random basis, b':  [1 1 0 0 0 1 0 1 1 0 0 0 1 1 1 1]
Eve has chosen random basis:  [1 1 0 1 0 1 0 1 0 1 1 1 1 0 1 1]
Simulating...
Bob's measurement result:  [0 1 0 0 1 0 1 1 0 1 1 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 0 1 1 0 0 0 1 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [0 0 0 1]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [0 0 0 1]
Interference detected... Aborting!
Simulation round: 53
Alice has generated random secret data bits, a:  [0 1 1 0 0 0 0 1 1 1 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 0]
Bob has chosen random basis, b':  [1 0 1 1 1 0 1 1 1 0 0 1 1 0 1 1]
Eve has chosen random basis:  [1 0 1 1 0 0 0 0 1 0 0 1 0 0 1 1]
Simulating...
Bob's measurement result:  [1 1 0 0 0 0 0 0 1 1 0 1 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 1 1 0 0 0 0 1 1 1 0 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 54
Alice has generated random secret data bits, a:  [0 0 1 0 1 1 1 1 1 0 1 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 1 0 1 1 1 1 1 1 1 1 0]
Bob has chosen random basis, b':  [1 1 0 1 1 0 1 0 0 1 1 1 1 0 1 1]
Eve has chosen random basis:  [0 1 1 0 0 0 1 0 0 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 1 1 0 0 0 1 1 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 0 1 0 1 0 1 0 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [1 1 0 1]
Interference detected... Aborting!
Simulation round: 55
Alice has generated random secret data bits, a:  [0 0 0 1 1 1 1 0 1 1 1 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 1 0 0 1 1 0 0 1 1 1 0]
Bob has chosen random basis, b':  [1 1 0 1 1 0 0 0 0 1 0 1 1 1 0 0]
Eve has chosen random basis:  [1 1 1 0 0 0 0 1 1 1 0 1 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 1 1 1 1 1 0 1 1 1 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 0 1 1 0 1 1 1 0 1 1 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [1 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 56
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 0 1 0 0 1 1 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 0 0 1 1 1 1 1 0 0 0 1 0]
Bob has chosen random basis, b':  [0 0 0 1 1 0 1 0 1 1 1 0 1 0 1 0]
Eve has chosen random basis:  [1 0 0 0 0 1 0 1 0 1 1 0 0 1 1 0]
Simulating...
Bob's measurement result:  [0 1 0 1 1 0 0 0 0 0 1 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 0 0 1 0 0 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [1 1 0 1]
Simulation round: 57
Alice has generated random secret data bits, a:  [1 1 1 0 1 0 0 0 0 1 1 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 0 1 0 1 1 0 0 1 0 0 0]
Bob has chosen random basis, b':  [1 0 0 0 0 0 1 1 0 1 0 1 1 1 0 1]
Eve has chosen random basis:  [1 0 0 1 0 0 1 0 1 0 0 0 0 0 1 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 0 0 0 1 1 1 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 0 1 0 0 1 1 1 0 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [1 1 0 1]
Simulation round: 58
Alice has generated random secret data bits, a:  [1 0 1 1 1 0 0 1 1 0 1 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 0 1 0 0 1 1 1 0 0 0 1]
Bob has chosen random basis, b':  [0 1 1 1 1 1 1 1 0 1 0 0 1 0 1 1]
Eve has chosen random basis:  [0 0 1 1 1 0 0 0 1 0 0 0 0 0 1 0]
Simulating...
Bob's measurement result:  [1 0 1 0 0 1 0 1 1 0 1 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 0 0 0 0 0 0 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [1 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Interference detected... Aborting!
Simulation round: 59
Alice has generated random secret data bits, a:  [0 1 1 1 0 1 0 0 1 1 0 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 0 0 0 0 0 0 1 1 1 0 0 0]
Bob has chosen random basis, b':  [0 1 0 0 0 1 0 0 1 1 0 1 0 0 0 0]
Eve has chosen random basis:  [0 1 0 1 1 1 0 0 1 1 0 0 0 1 1 0]
Simulating...
Bob's measurement result:  [0 1 1 1 0 1 0 0 1 0 1 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 1 0 0 1 1 0 1 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 0 1 0]
Interference detected... Aborting!
Simulation round: 60
Alice has generated random secret data bits, a:  [0 1 1 1 1 1 0 0 1 0 0 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 0 0 1 1 0 1 0 0 1 0 0]
Bob has chosen random basis, b':  [0 1 0 0 1 1 1 1 1 0 1 0 1 0 1 1]
Eve has chosen random basis:  [0 1 1 0 1 1 1 0 1 1 0 0 1 0 0 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 0 1 0 1 0 0 0 0 1 0 1]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 1 0 0 1 1 0 0 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 0 0]
Successfully exchanged private key:  [1 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 1 0]
Interference detected... Aborting!
Simulation round: 61
Alice has generated random secret data bits, a:  [0 0 0 1 1 1 1 1 1 0 1 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 0 1 0 0 1 0 0 0 0 1 1]
Bob has chosen random basis, b':  [0 0 1 1 0 1 1 0 0 1 1 1 0 1 0 0]
Eve has chosen random basis:  [1 0 1 0 1 1 0 1 1 0 1 1 1 0 0 1]
Simulating...
Bob's measurement result:  [1 0 0 1 1 0 1 1 1 0 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 1 1 0 0 0 1 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 62
Alice has generated random secret data bits, a:  [1 0 1 1 1 1 0 1 1 0 1 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 1 0 1 1 1 1 0 1 1 0 0 1]
Bob has chosen random basis, b':  [0 1 0 0 1 1 1 0 0 1 1 1 0 0 1 0]
Eve has chosen random basis:  [0 1 0 1 1 0 0 1 1 1 1 1 1 1 0 1]
Simulating...
Bob's measurement result:  [1 0 1 1 1 1 0 1 1 0 0 0 1 1 1 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 0 0 0 1 1 0 1 0 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [0 0 0 1]
Simulation round: 63
Alice has generated random secret data bits, a:  [1 0 1 0 1 1 0 0 1 0 1 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 1 1 1 0 0 1 1 0 1 0 1]
Bob has chosen random basis, b':  [1 1 0 1 1 0 1 1 1 1 0 0 1 0 1 0]
Eve has chosen random basis:  [1 0 0 0 0 1 1 1 1 0 1 0 0 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 1 1 1 0 0 0 1 1 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 1 0 1 0 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [0 1 1 0]
Interference detected... Aborting!
Simulation round: 64
Alice has generated random secret data bits, a:  [0 0 1 1 1 1 1 0 0 1 0 0 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 0 1 1 1 1 1 0 0 1 1 1]
Bob has chosen random basis, b':  [0 0 1 1 0 1 1 1 1 1 0 1 0 0 1 0]
Eve has chosen random basis:  [1 0 1 0 0 1 1 1 1 1 1 0 1 0 0 0]
Simulating...
Bob's measurement result:  [1 0 1 1 1 1 1 0 0 1 1 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 1 1 0 0 0 0 1 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 65
Alice has generated random secret data bits, a:  [1 1 1 0 1 1 0 1 1 1 1 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 0 1 1 0 0 0 1 1 1 1 0 1]
Bob has chosen random basis, b':  [0 0 0 1 0 1 1 1 1 0 1 1 0 1 0 0]
Eve has chosen random basis:  [1 1 1 0 1 0 0 0 1 1 1 0 0 0 1 1]
Simulating...
Bob's measurement result:  [1 1 1 0 1 1 0 0 1 1 1 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [0 1 1 0 0 1 0 1 1 0 1 0 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [1 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [0 0 0 1]
Interference detected... Aborting!
Simulation round: 66
Alice has generated random secret data bits, a:  [0 0 1 1 1 1 0 0 1 0 1 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 1 1 0 1 1 1 1 1 1 0 1]
Bob has chosen random basis, b':  [1 0 0 0 0 1 1 0 1 1 0 1 1 0 0 1]
Eve has chosen random basis:  [1 1 0 1 1 1 1 1 0 0 1 0 0 0 0 1]
Simulating...
Bob's measurement result:  [1 0 1 0 1 1 0 0 1 0 1 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 0 1 1 1 0 1 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [0 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 0 0]
Successfully exchanged private key:  [0 1 0 1]
Simulation round: 67
Alice has generated random secret data bits, a:  [0 1 1 1 0 0 1 1 0 1 0 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 1 0 1 0 1 0 0 1 0 1 1]
Bob has chosen random basis, b':  [1 0 1 1 1 0 1 0 0 0 0 0 0 0 1 1]
Eve has chosen random basis:  [0 1 1 1 0 1 0 0 1 1 1 1 0 0 1 1]
Simulating...
Bob's measurement result:  [0 1 1 0 1 0 0 1 0 1 0 1 0 1 0 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 0 0 0 1 1 1 0 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 68
Alice has generated random secret data bits, a:  [1 0 0 0 1 0 0 0 1 0 1 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 0 0 0 0 0 0 0 1 0 1 1]
Bob has chosen random basis, b':  [1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1]
Eve has chosen random basis:  [1 0 0 0 1 0 0 1 1 0 1 1 0 0 1 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 0 0 1 1 0 1 1 0 1 0 1]
Bob's measurement result with eavesdropping:  [1 1 0 0 1 0 1 0 1 0 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [0 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Interference detected... Aborting!
Simulation round: 69
Alice has generated random secret data bits, a:  [1 1 1 1 1 0 1 0 0 0 1 0 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 1 1 0 0 0 1 0 1 0 1 1]
Bob has chosen random basis, b':  [0 1 0 1 1 0 1 1 1 0 1 0 1 1 1 1]
Eve has chosen random basis:  [1 0 0 0 1 0 1 1 0 0 0 0 0 0 0 1]
Simulating...
Bob's measurement result:  [1 1 0 0 0 0 1 1 0 0 1 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 0 0 0 1 0 1 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [0 1 0 0]
Interference detected... Aborting!
Simulation round: 70
Alice has generated random secret data bits, a:  [1 0 0 1 1 1 1 0 1 0 1 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 0 0 0 0 0 0 0 1 0 0 0 0]
Bob has chosen random basis, b':  [0 1 1 1 0 1 0 0 0 0 0 1 0 0 0 1]
Eve has chosen random basis:  [0 0 1 1 0 0 0 1 1 0 0 1 0 0 0 1]
Simulating...
Bob's measurement result:  [1 0 0 1 1 1 1 0 1 0 1 0 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 1 1 0 0 0 1 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [0 1 1 1]
Simulation round: 71
Alice has generated random secret data bits, a:  [0 0 0 1 1 1 1 0 0 1 1 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 1 0 0 1 1 1 0 1 0 0 0]
Bob has chosen random basis, b':  [0 1 1 1 0 0 1 1 1 0 1 0 0 0 0 1]
Eve has chosen random basis:  [1 0 0 0 0 1 1 0 0 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 1 0 1 0 0 1 1 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 1 1 1 0 1 1 1 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [1 0 0 0]
Interference detected... Aborting!
Simulation round: 72
Alice has generated random secret data bits, a:  [1 0 1 1 1 0 1 1 1 0 1 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 1 1 1 1 0 1 1 1 0 0 1]
Bob has chosen random basis, b':  [0 1 0 1 0 1 1 1 0 1 1 1 0 0 0 1]
Eve has chosen random basis:  [0 1 1 1 0 1 0 0 0 0 1 0 0 1 0 1]
Simulating...
Bob's measurement result:  [1 1 1 1 0 0 1 1 0 0 1 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 0 1 1 1 0 1 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 73
Alice has generated random secret data bits, a:  [0 1 1 1 0 0 0 0 1 0 1 1 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 1 1 0 1 0 1 1 0 1 0 1]
Bob has chosen random basis, b':  [1 0 0 1 1 0 1 1 0 0 1 1 0 1 1 1]
Eve has chosen random basis:  [0 0 0 0 0 0 0 0 1 1 1 0 0 1 0 1]
Simulating...
Bob's measurement result:  [0 1 1 1 0 1 0 0 1 0 1 1 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 0 0 1 1 1 1 1 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 74
Alice has generated random secret data bits, a:  [1 0 0 1 1 0 1 0 0 0 0 1 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 0 1 1 0 1 1 0 0 0 1 0]
Bob has chosen random basis, b':  [0 1 1 1 1 0 1 1 0 0 1 0 0 0 1 1]
Eve has chosen random basis:  [0 1 0 1 0 1 1 0 1 0 0 1 1 0 1 1]
Simulating...
Bob's measurement result:  [1 0 0 1 1 0 1 0 0 1 0 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 0 0 0 0 1 0 1 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 0]
Interference detected... Aborting!
Simulation round: 75
Alice has generated random secret data bits, a:  [1 1 1 1 0 0 0 0 1 1 0 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 1 1 0 0 0 0 0 1 0 0 1]
Bob has chosen random basis, b':  [0 0 1 1 1 1 0 1 1 1 1 0 1 1 1 0]
Eve has chosen random basis:  [0 1 1 1 0 0 1 0 1 0 0 0 1 0 0 0]
Simulating...
Bob's measurement result:  [1 1 0 0 0 0 0 0 1 0 1 1 1 0 0 1]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 0 0 1 1 0 1 1 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [1 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [0 0 1 1]
Interference detected... Aborting!
Simulation round: 76
Alice has generated random secret data bits, a:  [1 1 1 0 0 1 0 0 0 0 1 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 1 1 0 0 1 0 0 1 0 1 1]
Bob has chosen random basis, b':  [1 1 0 1 1 0 1 0 1 0 0 1 0 0 0 1]
Eve has chosen random basis:  [1 1 1 1 1 0 0 0 1 0 1 1 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 0 0 1 0 0 1 0 1 1 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 1 0 0 0 0 0 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 1 0 0]
Interference detected... Aborting!
Simulation round: 77
Alice has generated random secret data bits, a:  [0 1 0 1 0 1 0 1 0 1 0 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 1 0 0 1 0 1 0 1 1 1 1 1]
Bob has chosen random basis, b':  [0 0 1 0 1 1 1 1 0 1 0 0 1 1 1 0]
Eve has chosen random basis:  [1 0 0 1 1 1 0 0 1 0 0 1 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 1 1 0 0 0 1 0 1 0 1 0 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 1 1 1 0 1 0 0 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Interference detected... Aborting!
Simulation round: 78
Alice has generated random secret data bits, a:  [1 1 1 1 0 1 1 0 1 0 1 1 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 0 0 1 1 1 1 1 0 1 0 1 1]
Bob has chosen random basis, b':  [1 0 1 0 1 0 1 0 1 0 1 1 0 0 0 1]
Eve has chosen random basis:  [0 1 1 1 0 1 0 0 1 1 1 0 0 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 0 1 1 1 0 1 1 1 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 0 0 1 1 1 0 0 1 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [1 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 0 1]
Interference detected... Aborting!
Simulation round: 79
Alice has generated random secret data bits, a:  [1 1 1 1 1 0 1 1 1 0 1 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 1 1 0 1 1 1 0 1 1 1 1 0]
Bob has chosen random basis, b':  [1 1 0 0 0 0 1 1 0 0 0 1 0 1 0 1]
Eve has chosen random basis:  [1 0 0 1 0 1 0 1 1 0 0 0 1 1 0 0]
Simulating...
Bob's measurement result:  [1 1 1 1 1 1 0 1 0 1 1 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 1 0 1 0 1 0 1 0 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 0 1]
Interference detected... Aborting!
Simulation round: 80
Alice has generated random secret data bits, a:  [1 1 1 0 1 1 1 0 0 1 1 0 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 1 1 0 1 0 0 1 1 1 0 0]
Bob has chosen random basis, b':  [1 1 1 0 0 0 0 0 1 0 1 0 0 0 1 0]
Eve has chosen random basis:  [1 1 1 0 0 0 0 1 1 1 1 1 0 1 1 0]
Simulating...
Bob's measurement result:  [1 1 1 1 0 1 1 0 0 1 0 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 0 0 1 0 1 1 0 1 1 1 0 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [0 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [0 0 0 1]
Interference detected... Aborting!
Simulation round: 81
Alice has generated random secret data bits, a:  [0 1 0 0 0 1 0 0 1 1 1 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 1 1 0 0 1 0 0 1 1 0 0]
Bob has chosen random basis, b':  [0 1 0 1 1 0 1 0 1 0 1 1 0 0 0 0]
Eve has chosen random basis:  [0 0 1 0 0 0 0 1 1 0 1 0 0 0 0 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 0 0 0 1 1 0 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 1 0 0 1 1 1 1 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 0 0]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 0 0]
Interference detected... Aborting!
Simulation round: 82
Alice has generated random secret data bits, a:  [1 1 0 0 0 0 0 0 1 1 1 0 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 0 1 1 1 1 0 1 1 0 0 0]
Bob has chosen random basis, b':  [1 0 0 0 1 1 0 1 1 0 1 0 1 0 1 1]
Eve has chosen random basis:  [0 1 0 1 1 0 1 1 1 1 0 0 0 1 0 1]
Simulating...
Bob's measurement result:  [0 0 0 0 0 1 0 0 1 1 1 1 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 0 1 1 0 0 1 1 1 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [0 0 0 1]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 1]
Bob has check bits:  [0 1 0 1]
Interference detected... Aborting!
Simulation round: 83
Alice has generated random secret data bits, a:  [0 1 1 1 1 1 0 1 1 0 0 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 1 0 0 1 0 0 1 0 0 0 1]
Bob has chosen random basis, b':  [1 0 0 1 0 1 0 1 1 1 1 1 0 0 1 1]
Eve has chosen random basis:  [1 0 0 1 1 0 0 0 0 1 0 0 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 1 1 0 1 0 1 1 1 1 1 0 0 0 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 1 0 1 1 0 1 1 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [1 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 84
Alice has generated random secret data bits, a:  [1 0 1 0 1 1 0 0 0 0 1 0 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 1 0 0 0 0 1 1 1 1 1 0]
Bob has chosen random basis, b':  [1 1 0 0 1 0 1 1 0 0 0 1 1 1 1 0]
Eve has chosen random basis:  [0 1 1 1 1 1 0 0 0 0 0 1 0 1 1 0]
Simulating...
Bob's measurement result:  [1 0 1 0 1 1 1 1 0 0 1 0 1 0 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 1 0 0 0 0 1 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 0 0 0]
Interference detected... Aborting!
Simulation round: 85
Alice has generated random secret data bits, a:  [0 0 0 0 0 0 1 0 1 1 0 1 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 0 1 0 1 1 0 0 0 1 1]
Bob has chosen random basis, b':  [1 0 0 1 0 0 1 1 0 1 0 1 0 1 0 1]
Eve has chosen random basis:  [0 1 0 0 1 0 1 1 1 1 0 1 0 1 1 1]
Simulating...
Bob's measurement result:  [0 0 0 1 0 1 0 0 1 1 0 1 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 0 0 1 1 0 1 1 1 0 1 1 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 0 0]
Successfully exchanged private key:  [1 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 0 0]
Bob has check bits:  [0 0 1 1]
Interference detected... Aborting!
Simulation round: 86
Alice has generated random secret data bits, a:  [1 0 0 1 1 1 1 1 1 1 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 1]
Bob has chosen random basis, b':  [1 0 1 1 1 1 0 0 0 1 0 0 0 0 1 1]
Eve has chosen random basis:  [1 0 1 0 1 1 1 1 1 0 0 1 0 1 1 1]
Simulating...
Bob's measurement result:  [0 0 0 1 1 0 1 1 1 0 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 0 0 1 1 1 1 1 1 0 1 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 87
Alice has generated random secret data bits, a:  [0 1 0 1 0 1 1 1 1 1 1 1 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 0 0 1 1 0 0 0 0 0 1 1]
Bob has chosen random basis, b':  [0 0 1 0 1 0 0 1 0 0 0 1 0 1 0 1]
Eve has chosen random basis:  [0 1 0 0 0 0 0 1 1 0 1 1 0 1 0 0]
Simulating...
Bob's measurement result:  [0 1 1 0 0 1 1 1 0 1 1 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 1 1 1 1 0 1 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 88
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 1 0 1 0 1 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 0 0 1 1 1 1 1 0 0 1 1 0]
Bob has chosen random basis, b':  [0 1 1 0 1 0 0 0 1 1 1 1 1 1 1 0]
Eve has chosen random basis:  [0 0 1 1 1 0 0 0 0 1 1 1 1 1 0 1]
Simulating...
Bob's measurement result:  [0 1 1 0 0 0 1 1 1 0 1 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 0 1 0 1 1 1 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 1]
Interference detected... Aborting!
Simulation round: 89
Alice has generated random secret data bits, a:  [0 0 0 1 0 1 1 0 0 1 0 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 0 1 1 1 0 1 0 0 0 1 0]
Bob has chosen random basis, b':  [0 0 0 0 1 0 0 1 1 0 1 1 0 1 0 0]
Eve has chosen random basis:  [0 1 0 0 0 0 0 1 0 1 0 1 1 1 0 0]
Simulating...
Bob's measurement result:  [0 1 0 1 1 1 1 0 0 1 0 1 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 1 1 0 0 1 0 1 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 0 1 0]
Simulation round: 90
Alice has generated random secret data bits, a:  [0 0 1 1 0 0 1 0 1 0 0 0 1 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 0 1 1 1 0 1 1 1 0 1 0 0]
Bob has chosen random basis, b':  [1 0 1 0 0 1 0 1 1 1 1 0 0 0 1 1]
Eve has chosen random basis:  [1 0 0 1 1 0 0 0 1 1 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 0 1 1 0 0 1 0 0 0 0 1 1 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 0 1 0 1 1 0 0 1 0 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 0 0]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 0 0]
Interference detected... Aborting!
Simulation round: 91
Alice has generated random secret data bits, a:  [1 1 0 0 0 1 0 0 0 0 1 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 1 1 0 1 0 1 0 1 0 0]
Bob has chosen random basis, b':  [1 0 1 0 1 1 0 0 0 1 0 0 0 0 0 1]
Eve has chosen random basis:  [0 0 1 1 1 0 1 1 1 1 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [1 1 0 0 1 1 1 1 0 0 1 1 1 0 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 0 0 1 0 0 1 0 1 1 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [0 1 1 1]
Simulation round: 92
Alice has generated random secret data bits, a:  [0 1 0 1 1 1 1 0 1 0 0 1 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 1 0 0 0 0 0 1 1 0 1 0]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 0 0 1 1 1 1 0 1 1]
Eve has chosen random basis:  [1 0 1 0 1 0 0 0 1 1 1 1 1 0 0 1]
Simulating...
Bob's measurement result:  [0 0 0 1 0 0 0 0 1 0 1 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 0 0 0 0 0 0 1 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 1 1 0]
Interference detected... Aborting!
Simulation round: 93
Alice has generated random secret data bits, a:  [0 0 1 1 0 1 0 1 1 1 0 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 1 0 1 1 1 0 0 0 1 1 1]
Bob has chosen random basis, b':  [0 0 1 0 1 1 0 0 0 0 0 1 1 0 0 1]
Eve has chosen random basis:  [0 0 1 0 0 0 1 0 1 1 1 0 0 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 0 1 0 0 0 1 0 0 1 1 0 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 0 1 1 1 1 1 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [1 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 1]
Interference detected... Aborting!
Simulation round: 94
Alice has generated random secret data bits, a:  [1 1 0 1 0 1 1 0 1 0 1 1 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 1 1 1 1 0 1 0 0 1 0 1 1]
Bob has chosen random basis, b':  [0 1 1 1 1 1 1 1 1 1 0 1 1 0 1 0]
Eve has chosen random basis:  [0 1 0 0 0 1 1 1 1 1 0 0 1 1 0 0]
Simulating...
Bob's measurement result:  [1 1 0 1 0 1 1 0 1 0 1 0 0 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 0 1 1 1 1 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [1 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [1 0 1 1]
Simulation round: 95
Alice has generated random secret data bits, a:  [0 0 1 0 0 0 1 1 1 1 0 1 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 1 1 1 1 1 1 1 1 0 0 0]
Bob has chosen random basis, b':  [0 1 0 1 0 1 1 0 0 1 1 0 1 0 0 0]
Eve has chosen random basis:  [1 0 1 1 0 0 1 1 1 0 0 0 1 1 0 0]
Simulating...
Bob's measurement result:  [1 0 0 1 0 0 1 0 1 1 0 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 0 1 1 1 1 0 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [0 1 1 0]
Simulation round: 96
Alice has generated random secret data bits, a:  [1 0 1 0 0 1 0 1 0 0 1 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 1 1 1 0 0 1 1 1 0 1 1]
Bob has chosen random basis, b':  [1 0 1 1 0 0 0 0 1 1 0 1 0 1 1 1]
Eve has chosen random basis:  [0 1 0 0 0 1 0 0 0 0 0 0 0 1 1 1]
Simulating...
Bob's measurement result:  [1 0 1 0 0 0 0 0 0 0 0 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 1 1 1 1 0 0 1 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Interference detected... Aborting!
Simulation round: 97
Alice has generated random secret data bits, a:  [0 1 1 1 0 1 1 0 1 1 1 0 0 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 1 0 1 1 0 0 1 1 1 1 1 0]
Bob has chosen random basis, b':  [0 1 1 1 0 1 1 1 0 1 1 1 0 0 0 1]
Eve has chosen random basis:  [1 0 0 0 0 0 0 1 0 1 1 1 0 0 0 0]
Simulating...
Bob's measurement result:  [1 0 1 1 1 0 1 0 1 0 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 0 0 1 0 1 1 1 1 1 0 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 98
Alice has generated random secret data bits, a:  [0 0 0 1 0 0 1 0 1 1 1 0 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 1 1 1 1 0 1 0 0 1 1 0 0 0]
Bob has chosen random basis, b':  [1 0 1 0 0 0 1 1 1 1 0 1 0 1 0 1]
Eve has chosen random basis:  [1 1 1 0 1 1 1 0 1 1 1 1 0 1 1 0]
Simulating...
Bob's measurement result:  [0 0 0 1 1 0 1 1 1 0 1 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 0 1 1 1 1 1 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 1]
Bob has check bits:  [0 0 1 1]
Successfully exchanged private key:  [1 1 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 1]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 99
Alice has generated random secret data bits, a:  [1 0 0 1 0 1 1 1 1 1 1 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 0 1 1 0 1 0 0 1 1 1 1]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 1 0 1 0 0 1 0 0 0]
Eve has chosen random basis:  [0 1 1 1 1 0 1 1 0 1 1 0 1 1 1 1]
Simulating...
Bob's measurement result:  [1 0 0 1 1 1 1 1 1 1 1 1 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 1 0 0 1 1 0 1 0 0 1 0 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [1 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 1 0]
Interference detected... Aborting!
Simulation round: 100
Alice has generated random secret data bits, a:  [0 1 0 1 1 0 1 1 0 0 0 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 0 0 0 1 1 0 0 0 1 1 1 0]
Bob has chosen random basis, b':  [1 0 1 0 0 1 1 0 0 1 1 0 0 1 0 0]
Eve has chosen random basis:  [0 1 0 0 0 0 1 1 0 1 0 0 1 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 0 0 1 0 1 0 0 1 0 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 1 0 1 1 1 0 1 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 0 0 1]
Simulation round: 101
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 1 1 1 1 0 1 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 0 1 0 0 0 0 1 0 0 1 1]
Bob has chosen random basis, b':  [0 0 0 0 0 1 0 1 1 0 1 0 0 1 0 1]
Eve has chosen random basis:  [0 0 1 1 0 1 0 1 1 0 1 1 1 0 1 1]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 1 1 1 1 0 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 1 0 1 0 0 1 1 1 1 0 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Interference detected... Aborting!
Simulation round: 102
Alice has generated random secret data bits, a:  [0 0 0 0 1 1 1 1 0 0 1 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 0 1 0 0 1 0 1 0 0 0 1 1]
Bob has chosen random basis, b':  [1 1 1 1 1 1 1 1 1 0 1 0 1 1 0 1]
Eve has chosen random basis:  [0 0 1 1 1 1 1 1 0 0 0 1 0 1 1 0]
Simulating...
Bob's measurement result:  [0 0 0 1 0 1 0 1 0 0 1 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [0 1 0 0 1 1 1 1 0 0 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [0 1 0 0]
Simulation round: 103
Alice has generated random secret data bits, a:  [1 1 1 0 1 0 0 0 0 0 1 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 1]
Bob has chosen random basis, b':  [0 1 1 1 0 1 0 1 1 1 0 0 1 0 0 1]
Eve has chosen random basis:  [0 0 0 1 1 1 1 1 0 0 1 1 1 1 0 1]
Simulating...
Bob's measurement result:  [1 1 0 0 1 0 1 0 0 0 0 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 0 0 0 0 0 1 1 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Interference detected... Aborting!
Simulation round: 104
Alice has generated random secret data bits, a:  [1 1 1 1 1 0 0 1 1 1 1 1 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 1 0 1 0 0 1 1 0 0 1 1 1]
Bob has chosen random basis, b':  [1 0 0 0 1 0 0 0 1 1 1 1 0 0 1 0]
Eve has chosen random basis:  [0 1 1 0 0 1 1 1 0 0 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [1 0 1 1 1 0 1 1 1 1 1 0 1 1 0 1]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 0 0 1 1 1 1 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 0]
Bob has check bits:  [1 1 1 0]
Interference detected... Aborting!
Simulation round: 105
Alice has generated random secret data bits, a:  [1 0 1 1 0 0 0 0 1 0 1 0 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 1 1 0 0 1 0 1 0 0 1 0 1]
Bob has chosen random basis, b':  [1 0 0 1 0 1 1 1 0 1 0 0 1 1 0 0]
Eve has chosen random basis:  [1 0 1 0 0 1 0 1 0 0 1 1 1 1 0 1]
Simulating...
Bob's measurement result:  [1 0 1 0 1 0 1 1 1 0 0 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 0 0 0 0 1 1 0 1 0 1 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 0 1]
Interference detected... Aborting!
Simulation round: 106
Alice has generated random secret data bits, a:  [0 0 1 1 0 1 1 0 0 0 1 1 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 0 1 1 1 1 0 0 0 1 0 0 0 0]
Bob has chosen random basis, b':  [0 1 0 0 1 1 0 0 1 1 0 1 1 1 0 1]
Eve has chosen random basis:  [1 1 0 0 1 0 0 0 0 0 1 1 0 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 0 1 1 1 1 1 1 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 1 0 0 0 1 1 1 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 107
Alice has generated random secret data bits, a:  [0 0 0 1 0 1 0 0 0 1 0 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 0 1 0 0 1 1 1 0 0 0 1]
Bob has chosen random basis, b':  [1 0 0 1 1 0 1 1 0 0 1 0 1 1 0 0]
Eve has chosen random basis:  [1 1 0 0 0 1 1 0 1 0 0 1 1 0 1 1]
Simulating...
Bob's measurement result:  [0 0 0 1 1 1 0 0 0 0 0 0 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 0 0 0 0 1 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 1]
Bob has check bits:  [0 0 1 1]
Successfully exchanged private key:  [0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 1]
Bob has check bits:  [1 1 1 0]
Successfully exchanged private key:  [0 0 0 1]
Simulation round: 108
Alice has generated random secret data bits, a:  [0 0 1 0 0 0 0 0 0 0 0 1 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 0 0 1 0 1 0 1 1 0 1 0 0]
Bob has chosen random basis, b':  [0 1 0 0 0 0 0 1 0 0 0 1 0 0 1 0]
Eve has chosen random basis:  [0 0 0 1 1 0 1 1 0 0 1 0 1 1 1 0]
Simulating...
Bob's measurement result:  [0 0 1 1 0 0 1 1 0 0 1 1 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 0 0 0 1 0 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 0 1 0]
Bob has check bits:  [0 0 1 0]
Interference detected... Aborting!
Simulation round: 109
Alice has generated random secret data bits, a:  [0 0 1 0 0 1 0 1 0 0 1 1 1 0 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 1 0 0 1 0 1 0 0 0 1 0 1]
Bob has chosen random basis, b':  [0 0 0 1 1 0 0 1 0 0 1 0 0 0 1 1]
Eve has chosen random basis:  [0 1 0 1 1 0 1 0 0 0 0 0 0 0 1 1]
Simulating...
Bob's measurement result:  [1 0 1 0 0 1 0 1 0 0 0 1 1 1 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 0 1 1 1 0 0 1 1 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 1 0 1]
Interference detected... Aborting!
Simulation round: 110
Alice has generated random secret data bits, a:  [0 0 1 1 1 1 0 1 0 0 0 0 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 0 0 1 1 1 1 1 0 0 0 0 1]
Bob has chosen random basis, b':  [1 0 0 0 1 0 0 1 1 0 0 0 0 0 1 1]
Eve has chosen random basis:  [0 0 1 1 0 0 1 0 1 1 1 0 1 1 0 1]
Simulating...
Bob's measurement result:  [1 0 0 1 0 1 0 1 0 1 1 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 0 1 0 1 1 0 0 0 0 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 0 1 1]
Interference detected... Aborting!
Simulation round: 111
Alice has generated random secret data bits, a:  [1 0 1 0 0 0 1 0 1 0 1 0 0 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 1 1 1 0 0 0 1 0 1 1 1 1]
Bob has chosen random basis, b':  [1 0 1 0 1 0 0 0 1 1 1 0 0 0 0 0]
Eve has chosen random basis:  [0 0 0 1 1 1 1 1 1 1 1 1 1 1 0 0]
Simulating...
Bob's measurement result:  [1 0 1 1 0 0 0 0 0 1 1 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 0 1 0 1 0 1 0 0 0 0 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 0 0 1]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 1]
Bob has check bits:  [1 1 0 0]
Interference detected... Aborting!
Simulation round: 112
Alice has generated random secret data bits, a:  [0 1 0 1 0 0 0 1 1 0 1 1 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 0 0 1 1 0 0 0 0 0 1 0 0 0]
Bob has chosen random basis, b':  [1 0 0 0 1 1 0 1 0 1 1 0 0 1 0 1]
Eve has chosen random basis:  [1 0 1 0 1 1 1 0 1 1 1 0 0 1 0 1]
Simulating...
Bob's measurement result:  [0 1 0 1 0 0 1 1 1 0 1 1 0 0 1 1]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 0 0 1 0 0 1 1 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [0 1 0 1]
Successfully exchanged private key:  [0 1 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 1]
Bob has check bits:  [1 1 0 0]
Interference detected... Aborting!
Simulation round: 113
Alice has generated random secret data bits, a:  [0 0 1 1 1 0 0 0 0 0 1 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 0 1 1 1 1 1 1 1 0 1 0 0 0]
Bob has chosen random basis, b':  [1 1 0 0 1 0 0 1 0 0 0 1 1 0 1 1]
Eve has chosen random basis:  [1 0 1 0 0 1 1 0 1 1 1 0 0 0 1 0]
Simulating...
Bob's measurement result:  [0 0 0 1 1 1 0 0 1 1 1 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 1 1 1 0 0 0 0 0 1 1 0 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 0]
Bob has check bits:  [0 1 1 0]
Successfully exchanged private key:  [1 0 0 0]
Simulation round: 114
Alice has generated random secret data bits, a:  [1 1 0 0 0 1 1 0 1 1 1 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1]
Bob has chosen random basis, b':  [0 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1]
Eve has chosen random basis:  [1 1 1 1 0 0 1 1 1 1 0 1 1 0 0 0]
Simulating...
Bob's measurement result:  [1 0 0 0 0 0 1 0 1 1 1 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 1 0 1 1 1 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [1 1 1 0]
Simulation round: 115
Alice has generated random secret data bits, a:  [1 0 1 0 1 1 0 1 1 0 0 1 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 0 1 1 1 1 1 0 1 1 1 1 0]
Bob has chosen random basis, b':  [0 1 0 0 1 1 1 0 0 0 0 0 0 1 1 1]
Eve has chosen random basis:  [1 1 0 0 1 0 1 1 1 0 1 0 0 0 1 0]
Simulating...
Bob's measurement result:  [1 0 1 0 1 1 0 1 0 0 0 1 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 1 1 1 1 1 1 0 1 1 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [0 0 1 1]
Interference detected... Aborting!
Simulation round: 116
Alice has generated random secret data bits, a:  [1 1 0 0 1 0 0 1 0 1 1 1 1 1 1 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 1 0 0 1 1 0 1 1 0 0 0 1 0]
Bob has chosen random basis, b':  [0 0 1 0 0 0 0 1 0 0 0 1 0 1 0 0]
Eve has chosen random basis:  [0 0 0 1 1 1 1 0 0 0 0 1 0 1 0 1]
Simulating...
Bob's measurement result:  [1 0 0 0 1 0 1 1 0 0 0 0 1 1 1 1]
Bob's measurement result with eavesdropping:  [1 0 1 0 1 1 0 1 0 0 1 1 1 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 1 0 1]
Successfully exchanged private key:  [1 0 1 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 1]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 117
Alice has generated random secret data bits, a:  [1 0 1 1 0 0 0 1 1 1 1 0 0 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 1 1 1 0 0 0 0 1 0 0 1 1]
Bob has chosen random basis, b':  [1 1 0 1 0 0 0 0 1 0 1 1 1 1 1 1]
Eve has chosen random basis:  [1 1 0 0 0 1 0 1 0 0 1 0 0 1 0 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 0 0 1 1 1 1 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [1 1 1 0 0 0 0 0 1 1 1 0 1 1 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [1 1 0 1]
Successfully exchanged private key:  [1 0 0 1]
Simulation round: 118
Alice has generated random secret data bits, a:  [1 1 1 1 0 1 1 0 0 0 1 1 1 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 1 1 0 1 1 0 1 0 0 0 1]
Bob has chosen random basis, b':  [0 1 0 0 1 0 0 1 0 1 1 1 1 0 1 1]
Eve has chosen random basis:  [1 0 0 0 1 0 1 0 1 1 0 1 1 0 1 0]
Simulating...
Bob's measurement result:  [1 1 1 1 1 0 1 1 0 0 0 1 1 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 0 1 1 0 0 1 0 1 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 119
Alice has generated random secret data bits, a:  [0 1 0 0 1 0 1 1 1 1 1 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 1 1 1 0 0 1 1 0 0 0 1 1 0 1 0]
Bob has chosen random basis, b':  [0 0 0 0 1 1 1 1 0 1 0 1 0 1 0 1]
Eve has chosen random basis:  [1 0 0 0 1 0 0 0 0 1 0 1 0 0 1 0]
Simulating...
Bob's measurement result:  [0 0 1 0 0 1 1 1 1 1 1 0 0 0 0 1]
Bob's measurement result with eavesdropping:  [0 0 0 1 1 0 1 1 1 1 1 1 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 1 1]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 120
Alice has generated random secret data bits, a:  [0 0 1 1 0 1 1 1 1 0 0 0 1 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 1 0 1 1 1 0 1 0 0 1 1 1 0]
Bob has chosen random basis, b':  [1 1 0 0 1 1 1 1 1 1 1 0 1 1 0 0]
Eve has chosen random basis:  [0 0 0 1 1 1 0 1 0 1 0 0 1 1 0 1]
Simulating...
Bob's measurement result:  [0 0 1 1 0 1 1 1 0 0 0 0 1 1 1 0]
Bob's measurement result with eavesdropping:  [1 0 1 1 0 1 1 0 1 1 1 0 1 0 0 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [0 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 0]
Interference detected... Aborting!
Simulation round: 121
Alice has generated random secret data bits, a:  [0 1 1 1 0 0 1 1 1 0 0 0 1 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 1 0 1 0 1 1 0 1 0 0 1 0 1 1 0]
Bob has chosen random basis, b':  [0 0 1 1 0 0 0 0 1 0 1 1 1 0 1 1]
Eve has chosen random basis:  [1 0 0 1 1 0 0 1 1 0 0 1 1 1 1 0]
Simulating...
Bob's measurement result:  [0 0 0 1 0 1 1 1 1 0 0 0 1 0 1 1]
Bob's measurement result with eavesdropping:  [0 1 0 0 0 1 1 1 0 0 0 0 1 0 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [1 0 1 1]
Successfully exchanged private key:  [1 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 1]
Bob has check bits:  [0 0 1 0]
Interference detected... Aborting!
Simulation round: 122
Alice has generated random secret data bits, a:  [0 1 1 0 0 1 1 1 0 0 0 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 1 0 1 0 0 1 1 1 0 1 0 0 0 0]
Bob has chosen random basis, b':  [0 0 0 0 1 0 1 0 0 0 1 1 0 1 0 0]
Eve has chosen random basis:  [0 0 1 1 1 0 1 0 1 0 1 1 1 1 1 0]
Simulating...
Bob's measurement result:  [0 1 0 0 0 1 0 1 1 0 1 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 0 1 1 1 0 1 0 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 0 0]
Successfully exchanged private key:  [0 0 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 0 0]
Bob has check bits:  [0 1 1 0]
Interference detected... Aborting!
Simulation round: 123
Alice has generated random secret data bits, a:  [1 0 1 1 1 1 1 0 1 1 0 0 0 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 1]
Bob has chosen random basis, b':  [0 0 1 1 0 0 1 0 1 1 0 1 1 0 1 0]
Eve has chosen random basis:  [0 1 0 1 0 0 1 0 1 1 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [1 0 1 1 1 1 0 0 1 0 0 0 1 0 0 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 1 1 1 0 0 1 0 0 1 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [1 1 1 1]
Interference detected... Aborting!
Simulation round: 124
Alice has generated random secret data bits, a:  [1 1 0 1 1 1 1 0 0 1 1 0 0 0 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 0 0 1 1 1 0 1 1 0 1 0 0 0 1 0]
Bob has chosen random basis, b':  [1 0 0 1 0 0 1 1 1 1 1 0 0 1 0 1]
Eve has chosen random basis:  [1 0 0 1 0 1 1 1 0 0 0 1 0 0 1 0]
Simulating...
Bob's measurement result:  [1 1 0 1 0 0 0 0 0 0 1 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 0 1 0 1 1 1 0 0 1 1 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 0]
Successfully exchanged private key:  [0 1 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 1 0]
Bob has check bits:  [1 0 1 1]
Interference detected... Aborting!
Simulation round: 125
Alice has generated random secret data bits, a:  [0 1 1 1 1 0 0 0 1 0 1 0 1 0 0 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 0 0 0 0 0 1 1 1 1 0 1 1 0 0]
Bob has chosen random basis, b':  [0 0 0 0 0 1 1 1 0 0 0 1 0 1 1 0]
Eve has chosen random basis:  [0 1 0 0 0 0 1 0 0 1 0 1 1 1 0 0]
Simulating...
Bob's measurement result:  [0 0 1 1 1 0 0 0 1 0 0 1 0 0 1 0]
Bob's measurement result with eavesdropping:  [0 1 1 1 1 0 0 0 1 0 0 0 1 1 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 0 0 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Interference detected... Aborting!
Simulation round: 126
Alice has generated random secret data bits, a:  [1 1 1 0 0 0 0 1 1 1 0 0 0 1 0 0]
She will arbitrarily encode these bits using random basis, b:  [1 0 1 1 1 0 0 0 0 1 0 0 1 0 0 1]
Bob has chosen random basis, b':  [1 0 0 1 1 1 1 0 1 1 1 1 0 0 1 1]
Eve has chosen random basis:  [1 1 0 0 0 1 1 1 1 0 1 1 1 1 1 0]
Simulating...
Bob's measurement result:  [1 1 1 0 0 1 0 1 1 1 0 1 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [1 1 0 0]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 1 0 0]
Bob has check bits:  [0 0 0 0]
Interference detected... Aborting!
Simulation round: 127
Alice has generated random secret data bits, a:  [0 0 1 1 1 0 1 1 1 0 0 1 1 1 0 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 1 1 0 0 1 1 1 1 0 0 1 0 0]
Bob has chosen random basis, b':  [0 0 0 1 1 1 1 1 1 0 0 1 1 1 0 1]
Eve has chosen random basis:  [1 1 1 1 1 0 1 1 0 0 1 0 0 1 1 1]
Simulating...
Bob's measurement result:  [0 0 1 1 1 0 0 1 1 0 0 1 1 1 0 0]
Bob's measurement result with eavesdropping:  [0 0 1 0 1 1 1 0 1 0 0 1 0 1 1 1]
Key Exchange without eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 1 1]
Successfully exchanged private key:  [1 1 1 0]
Key Exchange with eavesdropping: 
Alice has check bits:  [0 1 1 1]
Bob has check bits:  [0 1 0 1]
Interference detected... Aborting!
n= 4
Successful key exchanges without Eve present:  128
Successful key exchanges with Eve present:  24
Simulation round: 0
Alice has generated random secret data bits, a:  [1 0 1 1 0 0 0 0 0 0 1 0 1 1 1 1 0 0 1 0 1 0 1 0 0 1 0 0 0 1 1 0]
She will arbitrarily encode these bits using random basis, b:  [0 1 1 0 1 0 0 0 1 0 0 1 0 1 0 1 0 0 0 0 1 1 1 1 1 0 1 0 1 1 1 0]
Bob has chosen random basis, b':  [1 0 0 0 1 0 1 1 0 0 1 1 0 0 1 0 1 0 0 0 0 0 1 0 0 1 1 0 1 0 1 1]
Eve has chosen random basis:  [1 0 0 0 0 0 0 0 0 1 0 1 0 0 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 1 0 0]
Simulating...
Bob's measurement result:  [0 0 0 1 0 0 1 0 0 0 0 0 1 1 1 0 0 0 1 0 1 0 1 1 0 0 0 0 0 1 1 0]
Bob's measurement result with eavesdropping:  [1 1 1 1 0 0 0 1 1 1 0 0 1 0 1 1 0 0 1 0 0 1 0 0 0 0 0 0 0 1 1 0]
Key Exchange without eavesdropping: 
Alice has check bits:  [1 0 0 0 0 1 0 1]
Bob has check bits:  [1 0 0 0 0 1 0 1]
Successfully exchanged private key:  [0 1 0 1 0 0 0 1]
Key Exchange with eavesdropping: 
Alice has check bits:  [1 0 0 0 0 1 0 1]
Bob has check bits:  [1 0 0 1 0 1 0 1]
Interference detected... Aborting!
Simulation round: 1
Alice has generated random secret data bits, a:  [1 1 1 1 0 0 0 0 0 0 0 0 1 1 0 0 0 1 1 0 0 0 1 1 0 0 0 0 0 0 1 1]
She will arbitrarily encode these bits using random basis, b:  [1 0 0 0 0 1 1 0 1 1 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 1 0]
Bob has chosen random basis, b':  [1 1 1 1 0 1 0 0 1 1 0 1 1 0 0 1 1 1 1 0 1 1 0 0 0 1 0 1 1 0 0 0]
Eve has chosen random basis:  [1 1 0 1 1 0 1 0 0 1 1 1 0 1 0 0 0 1 0 0 0 0 1 0 1 1 1 1 0 1 0 1]
