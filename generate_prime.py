from random import randrange

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]

def nBitRandom(n):
    """ 
    Generation of random number of size n bit included in [2 ^ (n-1); 2^n-1]

    Args:
        n (int): size of bit

    Returns:
        int: a random integer
    """    
    return randrange(2**(n-1)+1, 2**n - 1)

def getLowLevelPrime(n):
    """
    Early "low level" removals.
    Return only primes that are "worthy" of passing MillerRabin's test, like a gate

    Args:
        n (int): the number of bits on which the number will be generated
    Returns:
        int: A integer worthy of passing the Miller Rabin test
    """    
    # """

    # """
    while True:
        pc = nBitRandom(n)
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                # If divisible by one of the prime in the list, test fail
                break
        else:
            return pc

def MillerRabin(n, k=5):
    """
    Prime test; Proballistic test.
    Chance that a non-prime number is taken as such: 4 ^ -k
    For the starting k (5) we are approaching a 0.0009765625% chance of hitting such a number.
    https://en.wikipedia.org/wiki/Miller–Rabin_primality_test
    
    Work with the idea of the Fermat's little theorem https://en.wikipedia.org/wiki/Fermat%27s_little_theore
    It is based on the fact that in a "field, which is the case of ℤ/pℤ" if p is prime, the equation x^2 = 1 has solutions only 1 and –1
    
    Args:
        n (int): The number to test
        k (int, optional): The number of iterations for testing is it is prime. Defaults to 5.

    Returns:
        [Bool]: Returns True if n is a strongly pseudo-prime number if k is to default, the chance for a composite to pass the test
                is equal to 0.0009765625%. Or in other world, the test is accurate to 0.9990234375% (We can increas K for better chance)
                If it composite return False
    """    
    if n < 2:return False  # Not prime (Composite)

    s, d = 0, n-1 
    while d % 2 == 0:
        s += 1 
        d //= 2 # Get a whole integer (and not a float)
    # s and d such that n - 1 = 2^s * d

    def isComposite(s, d):
        """
        Test if a number is composite (not prime) or not 

        Args:
            s (int): The result of the equation : n - 1 = 2^s * d
            d (int): The result of the equation : n - 1 = 2^s * d

        Returns:
            (Bool): True if it is a composite
                    False if it probably a prime
        """        
     
        a = randrange(2, n-1) # Random integer
        x = pow(a, d, n)  # x Integer remainder from dividing a^d by n

        if x == 1 or x == n-1:
            return False  # Probably a prime number

        for r in range(s-1):
            x = pow(x, 2, n)  # x Integer remainder from dividing x^2 by n
            if x == n-1: return False  # Probably a prime number
            if x == 1: return True  # Not prime (Composite)
        return True  # Not prime (Composite)

    for i in range(k): # Test for k time to increase the probability 
        if isComposite(s, d):
            return False  # Not prime (Composite)
    return True  # Probably a prime number 

def generate_prime(n=1024):
    """
    Generate a prime number of n bits

    Args:
        n (int, optional): The number of bits used to generate the prime. Defaults to 1024.

    Returns:
        Int: A probably prime number
    """    
    while True:
        prime_candidate = getLowLevelPrime(n)  # Filter out unpromising numbers
        if not MillerRabin(prime_candidate): continue
        else: break

    return prime_candidate


