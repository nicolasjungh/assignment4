import random

SymbolToNumber = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
NumberToSymbol = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}


def pattern_to_number(text):
    symboltonumber = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    erg = 0
    for k in range(len(text)):
        erg = 4 * erg + symboltonumber[text[k]]
    return erg


def number_to_pattern(index, k):
    if k == 1:
        return NumberToSymbol[index]
    erster_index = index // 4
    r = index % 4
    erstes_pattern = number_to_pattern(erster_index, k - 1)
    return erstes_pattern + NumberToSymbol[r]


def profil_wahrsch(text, k, profil):
    höchstwahrsch = 0
    kmer = text[0:k]
    for i in range(0, len(text) - k + 1):
        wahrsch = 1
        pattern = text[i:i+k]
        for j in range(k):
            l = SymbolToNumber[pattern[j]]
            wahrsch *= profil[l][j]
        if wahrsch > höchstwahrsch:
            höchstwahrsch = wahrsch
            kmer = pattern
    return kmer

def hammingDistance(s1, s2):
	hammer = 0
	for x, y in zip(s1, s2):
		if x != y:
			ham += 1
	return hammer

def distanceBetweenPatternAndString(pattern, dna):
	c = len(pattern)
	Abstand = 0
	for x in dna:
		Abstand = c+1
		for i in range(len(x) - c + 1):
			z = hammingDistance(pattern, x[i:i+c])
			if Abstand > z:
				Abstand = z
		distance = Abstand + 1
	return distance

def profil_form(motifs):
    k = len(motifs[0])
    profil = [[1 for i in range(k)] for j in range(4)]
    for x in motifs:
        for i in range(len(x)):
            j = SymbolToNumber[x[i]]
            profil[j][i] += 1
    for x in profil:
        for i in range(len(x)):
            x[i] = x[i]/len(motifs)
    return profil


def consensus(profil):
    str = ""
    for i in range(len(profil[0])):
        max = 0
        loc = 0
        for j in range(4):
            if profil[j][i] > max:
                loc = j
                max = profil[j][i]
        str += NumberToSymbol[loc]
    return str


def score(motifs):
    profil = profil_form(motifs)
    cons = consensus(profil)
    score = 0
    for x in motifs:
        for i in range(len(x)):
            if cons[i] != x[i]:
                score += 1
    return score


def random_motif_search(dna, k, t):
    bestMotifs = []
    motifs = []
    for x in range(0, t):
        random.seed()
        i = random.randint(0, len(dna[x])-k)
        motifs.append(dna[x][i:i+k])
    bestMotifs = motifs.copy()
    count = 0
    while True:
        profil = profil_form(motifs)
        for x in range(t):
            motifs[x] = profil_wahrsch(dna[x], k, profil)
        if score(motifs) < score(bestMotifs):
            bestMotifs = motifs.copy()
            count += 1
        else:
            print(count)
        return bestMotifs


k = 15
t = 20
dna = ["ACTTATATCTAGAGTAAAGCCCTGATTCCATTGACGCGATCCCTACCTCCATCATACTCCACAGGTTCTTCAATAGAACATGGGGAAAACTGAGGTACACCAGGTCTAACGGAGATTTCTGGCACTAACTACCCAAAATCGAGTGATTGAACTGACTTATATCTAGAGT", "AAAGCCCTGATTCCATTGACGCGATCCCTACCTCCATCATACTCCACAGGTTCTTCAATAGAACATGGGGAAAACTGAGGTACACCAGGTCTAACGGAGATTTCTGGCACTAACTACCCAAAATCCTCTCGATCACCGACGAGTGATTGAACTGACTTATATCTAGAGT", "CACTCCCGTCCGTCTGACGCCAGGTGCTCTACCCCGCTGATTGTCTGGTACATAGCAGCCTATAGATCACCGATGCAGAAACACTTCGAGGCAGCCGATTTCGCTTATCACAACGTGACGGAATTTGATAAACCACGTACTCTAATACCGTCACGGGCCCATCAACGAA", "ACAAGAACTGGTGGGGAGACTATGACACTCTAGCGGTCGCATAAGGGCCGGAAACCAGGACAAATCGATAAGATGAAGCGGGGATATAAGCCTTATACTGCGACTGGTTCCTTATATTATTTAGCCCCGATTGATCACCGATTAAAATATTCTGCGGTTTTCGAGACGG", "TAACCACACCTAAAATTTTTCTTGGTGAGATGGACCCCCGCCGTAAATATCAGGATTAAATGTACGGATACCCATGACCCTCCAGTCATCTACCTTCCCGTGGTGGTCGCTCAGCCTTGTGCAGACCGAACTAGCACCTGTCACATACAATGTTGCCCGCATAGATCGT", "ATCCGACAGAGGCAGTGAATAAGGTTTCGTTTCCTCAGAGAGTAGAACTGCGTGTGACCTTGCCTTCACCGACATCCGTTTCCAATTGAGCTTTTCAGGACGTTTAGGTAACTGATTGTCATTGCAATTGTCCGGGGGATTTAGATGGCCGGGTACCTCTCGGACTATA","CCTTGTTGCCACCGATTCGCGAGCAACATCGGAGTGCTCTGATTCACGGCGATGCTCCACGAAGAGGACCGCGGCACGACACGCCCTGTACCTACGTTTCTGGATATCCTCCGGCGAGTTAATAGAGCAATACGACCTGGTCGTCGAGATCGTGTATCTAGCCCTACCT","ATAGGTTAACGAATCAGGAGAGTTAATTTTACCTAGCTAGAGCGGACGGTGCCTGGCTGTATTCGCGTTTGACTTTCGGGCTCGCTGATAACTTGTGATCACCTTTTACGCTTACTGGATCCAACGATGGATCAAAGTTGAGAATTTCTGTGCCTTGGGTGTGAGCTGT","CTGACGAAAGGACGGGCGGTGTACTTAGTTTGGGGTAAAATAGTTGGTATAATTCTGTGCGACAGACATTTGGTCAGGCCATACTGCCATATCGTGATGTAACTATCCACACTACGTCATAGGCCCTTGTGATCAATTAAACGTTCCTCATGCCAGGCTATCTGTTTAA","GGCTTCGCGTTTAAGGCTGGATTAAGTACTCCGCCTTGTGATCTGTGATCCTCCGACCTGTGATCAGCAAGATTGGAACCTAGGTAGGCGGCGGGTCTACGCTGGCCCACAATCGTGAGTCCCCCACTCCGTAGGTTGTGGAATTTATAGACCCGCAAGGGGCACCACT","AGGATGACACCCAGGATGAATCTGGATTAGGAACACCAACCCGACATATTTGTTACCGCTGCAGCATTTCGCTCTTGGACGCGTAACCCGAGATCCGTCTCGCGATCGTCACGGATCGGGATTATGCAGGCAATACCTTGTGATCACTCCGCGCTTGGTTTTGCTAGCG","ACATCTCTAGTCACTTTTATTGAGCAGGTGGGCGGATTCATGATCCGGCTCTGTCGTACGTCCAACCACGGTGACATGTTCGGAGCTGTCGCCGTGGAGCAGAGATACATCGGATCTATCAATTTTACTAAGAGCAACTAGCCACGACAAACTGTGATCACCGATTGGA","AATTTGCGTATCTCTAGGACTCCCTCATACAAATCAAAGCTTGGATGGGTAAGATGCCGCAGCAGCAGGTATCTCATATTGGCTATTAAGAGCCAGGCCCTATGGCCTTAGTATCACCGATCAGACGTCGCATGAGCGGGCCCGTTGTCCTATCTCTTTAGCTGCCGCA","GAAGTAAAGGGGTTCCACTGCGTAGAGCGTGCCCCTCTGGTGTGCCGTACTGTTATGGTGATACAGCTTCCTTATACCCCTCGTAAAGCGGCTAATGGTCCTAATGAATGCCCTTGTGAAATCCGAATCGCTTTACAATTGCGTTCGGCGGAATGCAGTCACCAGTGTT","TACACTACGCGTTATTTACTTTTACTGAGTCCTTGTCGCCACCGAACGAGGATTGTTCATTGTATCCGGAGATTAGGAGTTCGCATCGCTGACACAGCCAGTTCGTAGCAAATACCGCTGGCCCTGGGCACTCCAGATCAGAACTACTAGCCCTAAACTCTATGACACA","TTGGGTCTCGATCCCTCTATGTTAAGCTGTTCCGTGGAGAATCTCCTGGGTTTTATGATTTGAATGACGAGAATTGGGAAGTCGGGATGTTGTGATCACCGCCGTTCGCTTTCATAAATGAACCCCTTTTTTTCAGCAGACGGTGGCCTTTCCCTTTCATCATTATACA","TTTCAAGTTACTACCGCCCTCTAGCGATAGAACTGAGGCAAATCATACACCGTGATCACCGACCCATGGAGTTTGACTCAGATTTACACTTTTAGGGGAACATGTTTGTCGGTCAGAGGTGTCAATTATTAGCAGATATCCCCCAACGCAGCGAGAGAGCACGGAGTGA","GATCCATTACCCTACGATATGTATATAGCGCCCTAGTACGGCTTCTCCCTTGCAGACACGCAGGCGCTGTGCGCTATCGGCTTCCTCGGACATTCCTGGATATAAGTAACGGCGAACTGGCTATCACTACCGCCGCTCCTTAAGCCTTGGTTTCACCGACGATTGTCGT","TAGTAGATTATTACCTGTGGACCGTTAGCTTCAAGACCGAAACGTTGGTGATGCTACTTAAATGTCAAGAGTTGCGAAGTTGGGCGAAGCACATCCGTACTCCCAAGTGGACGATCGATAGATCCATGGAGTTTCCATCCATCTTAATCCGCCCTTTGCATCACCGACG","TACAAGGCACAAACGAGACCTGATCGAACGGTGCACGGTCGAGGCAGCGAGATAAATGTACATTGAGAGCACCTTGTGATTTACGACCTGCATCGAAGGTTTCTTGGCACCCACCTGTCGTCCGCCAGGGCAGAGCCGACATTATATGACGCTGATGTACGAAGCCCCT"]
best = random_motif_search(dna, k, t)
min = score(best)
for x in range(100000):
	print(x)
	a = random_motif_search(dna, k, t)
	if score(a) < score(best):
		best= a
		min = score(a)
print(min)
for x in best:
    print(x)