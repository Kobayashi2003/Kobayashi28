
# define a exception class when unification fails
class UnificationError(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.message


class Term:

    __slots__ = ['type', 'name', 'args']

    __vars = ['x', 'y', 'z', 'u', 'v', 'w']

    def __init__(self, term: str):

        import re

        self.type = None
        self.name = None
        self.args = None

        var_const_pattern = re.compile(r'([a-z][a-z0-9_]*)')
        function_pattern = re.compile(r'([a-z][a-z0-9_]*)\((.*)\)')

        if function_pattern.match(term):
            # exm: 'f(g(x, y), z) -> ['f', FuncTerm('g(x, y)'), 'z']
            self.type = 'func'
            self.name = function_pattern.match(term).group(1)
            self.args = [Term(arg) for arg in (arg.strip() for arg in function_pattern.match(term).group(2).split(','))]
            if len(self.args) == 0:
                raise ValueError('The function has no arguments.')
        elif var_const_pattern.match(term):
            self.type = 'var' if term in self.__vars else 'const'
            self.name = term
        else:
            raise ValueError('The term is not in a valid form.')
                
    def __str__(self) -> str:
        if self.type == 'var' or self.type == 'const':
            return self.name
        elif self.type == 'func':
            return self.name + '(' + ', '.join([str(arg) for arg in self.args]) + ')'

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: 'Term|str') -> bool:

        if isinstance(other, str):
            other = Term(other)

        if self.type != other.type:
            return False
        if self.type == 'var' or self.type == 'const':
            return self.name == other.name
        elif self.type == 'func':
            if self.name != other.name:
                return False
            if len(self.args) != len(other.args):
                return False
            for i in range(len(self.args)):
                if self.args[i] != other.args[i]:
                    return False
            return True
        
    def __ne__(self, other: 'Term|str') -> bool:
        return not self.__eq__(other)
    
    def __contains__(self, var: 'Term|str') -> bool:

        if isinstance(var, str):
            var = Term(var)

        if self.type == 'var' or self.type == 'const':
            return self == var
        elif self.type == 'func':
            for arg in self.args:
                if arg.__contains__(var):
                    return True
            return False

        return False

    def __hash__(self) -> int:
        return hash(str(self))

    def is_var(self) -> bool:
        return self.type == 'var'

    def is_const(self) -> bool:
        return self.type == 'const'

    def is_func(self) -> bool:
        return self.type == 'func'

    def substitute(self, var: 'Term|str', term: 'Term|str') -> 'Term':
        # exm: f = Term('f(x, y)') -> f.substitute('x', 'f(z)') -> Term('f(f(z), y)')

        if isinstance(var, Term):
            var = str(var)
        if isinstance(term, Term):
            term = str(term)
        
        if self.type == 'const':
            raise ValueError('The term is a constant.')
        if self.type == 'var':
            return Term(term) if self.name == var else self
        if self.type == 'func':
            return Term(self.name + '(' + ', '.join([str(arg.substitute(var, term)) for arg in self.args]) + ')')


def most_general_unifier_recursion(atomic_rule1: str, atomic_rule2: str) -> dict:

    """Return the most general unifier of two atomic rules.
    Parameters:
        atomic_rule1: str
        atomic_rule2: str

    Return:
        unifier: dict
    """

    import re

    # term:
    # - a variable or a constant is a term
    # - if t1, t2, ..., tn are terms, and f is a function symbol of arity n, then f(t1, t2, ..., tn) is a term
    # - cause we only concern with first-order logic, predicate is not a term

    # variable naming convention:
    # - variables can only use names defined in vars

    # constant naming convention:
    # - start with a lowercase letter
    # - can only contain letters, numbers, and underscores

    # function naming convention:
    # - start with a lowercase letter
    # - can only contain letters, numbers, and underscores
    # - one or more terms separated by commas and enclosed in parentheses behind the function name

    # predicate naming convention: 
    # - start with a capital letter
    # - can only contain letters, numbers, and underscores
    # - one or more terms separated by commas and enclosed in parentheses behind the predicate name
    # sample: P(x, y), Q(f(x), g(y, z))

    # Strictly speaking, the regular expression here is not a strict predicate form, 
    # because in the specification, the predicate is started with a capital letter
    # But for the convenience of the subsequent recursive implementation of the function, 
    # the definition of the predicate is relaxed here
    pattern = re.compile(r'¬?([A-Za-z][A-Za-z0-9_]*)\((.*)\)')
    match1 = pattern.match(atomic_rule1)
    match2 = pattern.match(atomic_rule2)

    if match1 is None or match2 is None:
        raise UnificationError('The atomic rules are not in a valid form.')

    if match1.group(1) != match2.group(1):
        raise UnificationError('The predicates are different.')

    terms1 = [term.strip() for term in match1.group(2).split(',')]
    terms2 = [term.strip() for term in match2.group(2).split(',')]

    if len(terms1) == 0 or len(terms2) == 0:
        raise UnificationError('The atomic rules are not in a valid form.')

    if len(terms1) != len(terms2):
        raise UnificationError('The number of arguments is different.')

    terms1 = [Term(term) for term in terms1]
    terms2 = [Term(term) for term in terms2]

    unifier = {}
    error_msg = 'Error: Failed to unify the atomic rules.'
    for i in range(len(terms1)):
        if terms1[i] != terms2[i]:
            var_flg = terms1[i].is_var() + 2*terms2[i].is_var()
            if var_flg:
                var = terms1[i] if var_flg & 1 else terms2[i]
                term = terms2[i] if var_flg & 1 else terms1[i]
                if var in unifier and unifier[var] != term:
                    raise UnificationError(error_msg)
                if var in term:
                    raise UnificationError(error_msg)
                unifier[var] = term
            elif terms1[i].is_func() and terms2[i].is_func():
                unifier.update(most_general_unifier_recursion(str(terms1[i]), str(terms2[i])))
            else:
                raise UnificationError(error_msg)

    for key, value in unifier.items():
        for key2, value2 in unifier.items():
            if key != key2 and key in value2:
                unifier[key2] = value2.substitute(key, value)
               
    return unifier


def most_general_unifier(atomic_rule1: str, atomic_rule2: str) -> dict:

    """Return the most general unifier of two atomic rules.
    Parameters:
        atomic_rule1: str
        atomic_rule2: str

    Return:
        unifier: dict
    """

    try:
        unifier = most_general_unifier_recursion(atomic_rule1, atomic_rule2)
        return {str(key): str(value) for key, value in unifier.items()}
    except UnificationError as e:
        raise e


if __name__ == '__main__':

    atomic_rule1 = 'P(a, x, f(g(y)))'
    atomic_rule2 = 'P(z, f(z), f(g(u)))'

    try:
        unifier = most_general_unifier(atomic_rule1, atomic_rule2)
        print(unifier)
    except UnificationError as e:
        print(e)