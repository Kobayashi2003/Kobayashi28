from enum import Enum
import re


class TokenizeError(Exception):
    def __init__(self, message: str, position: int):
        self.message = message
        self.position = position
        super().__init__(f"Tokenize error at position {position}: {message}")

class ParserError(Exception):
    def __init__(self, message: str, position: int):
        self.message = message
        self.position = position
        super().__init__(f"Parser error at position {position}: {message}")


class TokenType(Enum):
    LPAREN = '('
    RPAREN = ')'
    AND = '+'
    OR = ','
    TERM = 'term'
    EOF = 'EOF'

class Token:
    def __init__(self, type: TokenType, value: str = None, position: int = 0):
        self.type = type
        self.value = value
        self.position = position

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0
        self.current_token = tokens[0]

    def advance(self) -> Token:
        """Advance to the next token."""
        self.current += 1
        if self.current < len(self.tokens):
            self.current_token = self.tokens[self.current]
        return self.current_token

    def peek(self) -> Token:
        """Look at the next token without consuming it."""
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return self.tokens[-1]

    def check(self, type: TokenType) -> bool:
        """Check if the current token is of the given type."""
        return self.current_token.type == type

    def match(self, type: TokenType) -> Token:
        """Match and consume the current token if it's of the given type."""
        if self.check(type):
            return self.advance()
        raise ParserError(
            f"Expected {type.value}, got {self.current_token.type.value}",
            self.current_token.position
        )

    def validate_expression(self) -> bool:
        """
        Validate the syntax of the expression.
        
        Grammar:
        expression ::= term (',' term)*
        term      ::= factor ('+' factor)*
        factor    ::= '(' expression ')'
                  |  term
        
        Returns:
            bool: True if the expression is syntactically valid
            
        Raises:
            ParserError: If the expression is invalid
        """
        try:
            self._validate_expression()
            # Check if we've reached the end of input
            if not self.check(TokenType.EOF):
                raise ParserError(
                    f"Unexpected token after expression: {self.current_token.type.value}",
                    self.current_token.position
                )
            return True
        except ParserError:
            return False

    def _validate_expression(self) -> None:
        """Validate an expression (OR level)."""
        self._validate_term()
        
        while self.check(TokenType.OR):
            self.match(TokenType.OR)
            self._validate_term()

    def _validate_term(self) -> None:
        """Validate a term (AND level)."""
        self._validate_factor()
        
        while self.check(TokenType.AND):
            self.match(TokenType.AND)
            self._validate_factor()

    def _validate_factor(self) -> None:
        """Validate a factor (parenthesized expression or term)."""
        if self.check(TokenType.LPAREN):
            self.match(TokenType.LPAREN)
            self._validate_expression()
            self.match(TokenType.RPAREN)
        elif self.check(TokenType.TERM):
            self.match(TokenType.TERM)
        else:
            raise ParserError(
                f"Unexpected token: {self.current_token.type.value}",
                self.current_token.position
            )


def normalize_expression(expression: str) -> str:
    """
    Normalize the expression by removing spaces around operators while preserving spaces within terms.
    
    Args:
        expression: The input expression to normalize
        
    Returns:
        The normalized expression
    """
    # Remove spaces around operators and parentheses
    normalized = re.sub(r'\s*\+\s*', '+', expression)
    normalized = re.sub(r'\s*,\s*', ',', normalized)
    normalized = re.sub(r'\s*\(\s*', '(', normalized)
    normalized = re.sub(r'\s*\)\s*', ')', normalized)
    
    return normalized

def tokenize(expression: str) -> list[Token]:
    """
    Tokenize the input expression into a list of tokens.
    
    Args:
        expression: The input string to tokenize
        
    Returns:
        list of Token objects
        
    Raises:
        ParserError: If invalid characters are found
    """
    tokens = []
    position = 0
    
    # Define token patterns
    patterns = {
        'LPAREN': r'\(',
        'RPAREN': r'\)',
        'AND': r'\+',
        'OR': r',',
        'TERM': r'[^\(\)\+,]+',  # Match any characters except ()+ and ,
    }
    
    # Create regex pattern
    pattern = '|'.join(f'(?P<{k}>{v})' for k, v in patterns.items())
    regex = re.compile(pattern)
    
    # Find all matches
    for match in regex.finditer(expression):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        start_pos = match.start()
        
        # Skip whitespace
        if start_pos > position:
            raise TokenizeError(f"Invalid characters at position {position}", position)
            
        tokens.append(Token(TokenType[token_type], token_value, start_pos))
        position = match.end()
    
    # Check for remaining characters
    if position < len(expression):
        raise TokenizeError(f"Invalid characters at position {position}", position)
    
    tokens.append(Token(TokenType.EOF, position=len(expression)))
    return tokens

def validate_logical_expression(expression: str) -> bool:
    """
    Validate the syntax of a logical expression.
    
    Args:
        expression: The input expression to validate
        
    Returns:
        bool: True if the expression is syntactically valid
    """
    try:
        normalized = normalize_expression(expression)
        tokens = tokenize(normalized)
        parser = Parser(tokens)
        return parser.validate_expression()
    except TokenizeError:
        return False
    except ParserError:
        return False


if __name__ == "__main__":
    # Test cases
    test_cases = [
        "Gang Rape + Unavoidable Rape", # Valid
        "(Gang Rape , Unavoidable Rape) + Netorare", # Valid
        "Gang Rape , Unavoidable Rape , Netorare", # Valid
        "Netorare + ((Completely Avoidable Rape, Unavoidable Rape) + Gang Rape)", # Valid
        "Gang Rape +", # Invalid
        "Gang Rape ,", # Invalid
        "(Gang Rape + Unavoidable Rape", # Invalid
        "Gang Rape + b)", # Invalid
        "Gang Rape + + b", # Invalid
        "Gang Rape , , b", # Invalid
    ]
    
    for expr in test_cases:
        print(f"\nExpression: {expr}")
        try:
            is_valid = validate_logical_expression(expr)
            print(f"Valid: {is_valid}")
        except Exception as e:
            print(f"Error: {e}")
