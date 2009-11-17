codelist = [
("''" , "621"), # hamza
("'u" , "624"), # hamza
("'w" , "624"), # hamza
("'I" , "625"), # hamza
("'i" , "626"), # hamza
("'A" , "623"), # hamza
("_A" , "622"), # long alef
('a'  , "64E"),
('A'  , "627"),
('b'  , "628"),
('t'  , "62A"),
('_t' , "62B"),
('j'  , "62C"),
('^g' , "62C"),
('.h' , "62D"),
('H'  , "62D"),
('_h' , "62E"),
('x'  , "62E"),
('d'  , "62F"),
('_d' , "630"),
('r'  , "631"),
('z'  , "632"),
('s'  , "633"),
('^s' , "634"),
('.s' , "635"),
('S'  , "635"),
('.d' , "636"),
('D'  , "636"),
('.t' , "637"),
('T'  , "637"),
('.z' , "638"),
('Z'  , "638"),
('`'  , "639"),
('3'  , "639"),
('.g' , "63A"),
('G'  , "63A"),
('f'  , "641"),
('q'  , "642"),
('k'  , "643"),
('l'  , "644"),
('m'  , "645"),
('n'  , "646"),
('h'  , "647"),
('u'  , "64F"),
('w'  , "648"),
('i'  , "650"),
('y'  , "64A"),
("'t" , "629"),# Taa Mabuta
('"' , "651"), # shadda
]

codes = {}

def setupcodes():
    global codes
    for key,val in codelist:
        if key in codes:
            raise "dupe code %s" % key
        codes[key] = val

setupcodes()

def arabise(instr):
    buff = unicode("", encoding="utf-8")
    while instr:
        code, instr = eatchar(instr)
        buff += code
    return buff
    #return revuni(buff)

def revuni(instr):
    l = list(instr)
    l.reverse()
    return u"".join(l)

def eatchar(instr):
    if not instr: raise "empty instr"
    if instr[0] in ("_",".","^","'"):
        off = 2
    else:
        off = 1
    ch = instr[0:off]
    rest = instr[off:]
    return (unichr(int(codes[ch],16)), rest)
    
def ar(ch):
    return unichr(int(ch,16))

def dumpall():
    for key,val in codes.items():
        print key, " ", unichr(int(val,16))


def test():
    print arabise("3ns")
    print arabise("bAb")
    print arabise("qlAm")

if __name__ == "__main__":
    test()
