from src.mfdfa.mfdfa import MFDFA


#mfdfa = MFDFA('(a+b)*b(a+1)b(a+b)*')
mfdfa = MFDFA('a*baa*ba*(ba*+1)')
mfdfa.print_doa()


'''mfdfa = MFDFA('(a+b)*(bb(a+b)*aa+bab)b*ba*')
print(mfdfa.contains('abaaaaabaaababbbbba'))
#mfdfa = DFA('(b(ba+a(ab)*b)*)*')
mfdfa.print_doa()'''

