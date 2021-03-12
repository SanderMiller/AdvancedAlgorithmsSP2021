from sympy import *
import copy


def DPLLSatSolver(CNF):
    '''
    Function to determine whether or not a CNF is satisfiable given 
    format (A v B v C) ^ (D v E) as [[A,B,C],[D,E]]
    '''
    #Create a deep copy of the CNF to edit
    CNFCopy = copy.deepcopy(CNF)

    #Check whether the CNF has any Unit Clauses or Pure Literals
    while checkUnitClauses(CNFCopy) or checkPureLits(CNFCopy):
        
        #If unit clauses exist in CNF
        if checkUnitClauses(CNFCopy):
    
            for clause in CNF:
                if len(clause) == 1:
                    #Define Literal and Not literal in Unit Clause
                    literal = clause[0]
                    notLiteral = ~literal
                    #Remove all Clauses with unit clause literal
                    CNFCopy = removeTrueClauses(CNFCopy, literal)
                    #Remove all instances of not literal from remaining CNF
                    CNFCopy = removeNotLiterals(CNFCopy,notLiteral)
        
        #If Pure Literals exist in CNF
        if checkPureLits(CNFCopy):
            
            #Generate list of all literals appearing in CNF
            allSymbols = allSymbolsInCNF(CNFCopy)

            #Identify and Remove all clauses with unique literal
            for lit in allSymbols:
                if ~lit not in allSymbols:
                    #Remove all Clauses with pure literal
                    CNFCopy = removeTrueClauses(CNFCopy, lit)

    #Check Base Cases
    if CNFCopy == []:
        return True
    if [] in CNFCopy:
        return False
    
    #Generate List of all literals in CNF, set first one to True
    allSymbols = allSymbolsInCNF(CNFCopy)
    #Remove All Clauses with newly assigned True literal
    NewCNF = removeTrueClauses(CNFCopy, allSymbols[0])
    #Remove all instances of ~literal from CNF
    NewCNF = removeNotLiterals(NewCNF,~allSymbols[0])

    #Try Solving Assignment
    if DPLLSatSolver(NewCNF):
        return True

    #Try assigning the literal to false
    else: 
        NewCNF = removeTrueClauses(CNFCopy, ~allSymbols[0])
        NewCNF = removeNotLiterals(NewCNF,allSymbols[0])

    result = DPLLSatSolver(CNFCopy)
    return result


def convert2Sym(Clause):
    '''
    Short Function converting my SAT list encoding to 
    SymPy's boolean encoding
    '''
    if Clause == []:
        return []
    ClauseSym = Clause[0]
    Clause2 = Clause.copy()
    Clause2.pop(0)
    for literal in Clause2:
        ClauseSym = Or(ClauseSym,literal)
    return ClauseSym

def checkUnitClauses(CNF):
    '''
    Function to determine if a Unit Clause
    Exists within a given CNF
    '''
    for clause in CNF:
        if len(clause) == 1:
            return True
    return False

def checkPureLits(CNF):
    '''
    Function to determine if a 
    Pure Literal Exists in a given CNF
    '''
    allSymbols = allSymbolsInCNF(CNF)
    for lit in allSymbols:
        if ~lit not in allSymbols:
            return True
    return False

def removeTrueClauses(CNF, literal):
    '''
    Function that given a CNF removes all clauses containing
    a given literal
    '''
    CNFCopy = copy.deepcopy(CNF)
    for clause in CNF:
        clauseSym = convert2Sym(clause)
        if literal in clause:
            CNFCopy.remove(clause)
    return CNFCopy

def removeNotLiterals(CNF, notLiteral):
    '''
    Function that given a CNF removes all instances 
    of ~literal
    '''
    for clause in CNF:
        if notLiteral in clause:
            clause.remove(notLiteral)
    return CNF

def allSymbolsInCNF(CNF):
    '''
    Function that given a CNF generates a list of 
    all literals within the CNF
    '''
    allSymbols = []
    for clause in CNF:
        for literal in clause:
            if literal not in allSymbols:
                allSymbols.append(literal)
    return allSymbols


    
if __name__ == "__main__":
    A,B,C,D = symbols('A,B,C,D')
    CNF1 = []
    CNF2 = [[A,~A]]
    CNF3 = [[A],[~A]]
    CNF4 = [[A,D],[C],[~A,B,A,~C], [B,D], [~C,A,B], [C,B], [~A,~D]]
    CNF5 = [[A,B,~C],[~A,~B,C],[~A,B,~C]]
    assert DPLLSatSolver(CNF1) == True
    assert DPLLSatSolver(CNF2) == True
    assert DPLLSatSolver(CNF3) == False
    assert DPLLSatSolver(CNF4) == True
    assert DPLLSatSolver(CNF5) == True
    print("No Assertion Errors")