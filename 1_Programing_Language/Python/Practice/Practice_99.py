def function(number: int, string: str) -> str:
    return string * number

func = lambda number : lambda string : function(number, string)

f = func(3)

print(f("Hello"))