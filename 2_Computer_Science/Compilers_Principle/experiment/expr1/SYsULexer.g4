lexer grammar SYsULexer;

// Keywords
Void : 'void';
Char : 'char';
Int : 'int';
Float : 'float';
Double : 'double';
Const : 'const';
Auto : 'auto';

If : 'if';
Else : 'else';
While : 'while';
For : 'for';
Do : 'do';
Break : 'break';
Continue : 'continue';
Return : 'return';

LeftParen : '(';
RightParen : ')';
LeftBracket : '[';
RightBracket : ']';
LeftBrace : '{';
RightBrace : '}';

Plus : '+';
Minus : '-';
Star : '*';
Slash : '/';
Percent : '%';
Exclaim : '!';
Amp : '&';
Pipe : '|';

PlusEqual : '+=';
MinusEqual : '-=';
StarEqual : '*=';
DivEqual : '/=';
PercentEqual : '%=';
ExclaimEqual : '!=';

AmpAmp : '&&';
PipePipe : '||';

Greater : '>';
Less : '<';
EqualEqual : '==';
GreaterEqual : '>=';
LessEqual : '<=';

Semi : ';';
Comma : ',';

Equal : '=';

Identifier
    :   IdentifierNondigit
        (   IdentifierNondigit
        |   Digit
        )*
    ;

fragment
IdentifierNondigit
    :   Nondigit
    ;

fragment
Nondigit
    :   [a-zA-Z_]
    ;

fragment
Digit
    :   [0-9]
    ;

Constant
    :   IntegerConstant
    ;

fragment
IntegerConstant
    :   DecimalConstant
    |   OctalConstant
    |   HexadecimalConstant
    ;

fragment
DecimalConstant
    :   NonzeroDigit Digit*
    ;

fragment
OctalConstant
    :   '0' OctalDigit*
    ;

fragment
HexadecimalConstant
    :   HexadecimalPrefix HexadecimalDigit*
    ;

fragment
NonzeroDigit
    :   [1-9]
    ;

fragment
OctalDigit
    :   [0-7]
    ;

fragment
HexadecimalPrefix
    :   '0' [xX]
    ;


fragment
HexadecimalDigit
    :   [0-9a-fA-F]
    ;


// 预处理信息处理，可以从预处理信息中获得文件名以及行号
// 预处理信息前面的数组即行号
LineAfterPreprocessing
    :   '#' Whitespace* ~[\r\n]*
//        -> skip
    ;

Whitespace
    :   [ \t]+
        -> skip
    ;

// 换行符号，可以利用这个信息来更新行号
Newline
    :   (   '\r' '\n'?
        |   '\n'
        )
        -> skip
    ;
