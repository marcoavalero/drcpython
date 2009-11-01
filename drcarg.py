class metaPrintCleaner(type):
    """
    I'm borrowing this method from page 120 of 'Python in a Nutshell', second edition
    """
    def __new__(mcl, classname, bases, classdict):
        def __init__(self, **kw):
            for k in self.__dflts__:setattr(self, k, self.__dflts__[k])
            for k in kw:setattr(self, k, kw[k])
        def __repr__(self):
            rep = ['%s=%r' %(k, getattr(self, k)) for k in self.__dflts__ if getattr(self, k) != self.__dflts__[k]]
            return '%s(%s)' %(classname, ', '.join(rep))
        def __str__(self):
            rep = ['%s' %(getattr(self, k)) for k in self.__dflts__ if getattr(self, k) != self.__dflts__[k]]
            return '<%s:%s>' %(classname,', '.join(rep))
        newdict = {'__slots__':[], '__dflts__':{}, '__init__':__init__, '__repr__':__repr__,'__str__':__str__,}
        for k in classdict:
            if k.startswith('__') and k.endswith('__'):
                if k in newdict:
                    warnings.warn("Can't set attr %r in print-cleaner%r") %(k, classname)
                else:
                    newdict[k] = classdict[k]
            else:
                newdict['__slots__'].append(k)
                newdict['__dflts__'][k] = classdict[k]
        return super(metaPrintCleaner, mcl).__new__(mcl, classname, bases, newdict)

class PrintCleaner(object):
    __metaclass__= metaPrintCleaner


class Str_Con(PrintCleaner):
    data = "None"
    type = "STRING"


class Int_Con(PrintCleaner):
    data = ""
    type = "INTEGER"

class DRC_Var(PrintCleaner):
    idid = "$"
    type = "UKNOWN"
    data = ""    
    free = True
    limited = True
    def __eq__(self, other):
        return self.idid == other.idid
    def __hash__(self):
        return sum(map(ord, self.idid))        
    def __ne__(self, other):
        return self.idid != other.idid

def verify(one, two):
    if one == two:
        return type_check(one, two)

def type_check(one, two):
    return one.type == two.type
