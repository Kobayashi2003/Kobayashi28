#include "SYsULexer.h" // 确保这里的头文件名与您生成的词法分析器匹配
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <regex>
#include <string>

// 映射定义，将ANTLR的tokenTypeName映射到clang的格式
std::unordered_map<std::string, std::string> tokenTypeMapping = {
  { "Void", "void" },
  { "Char", "char" },
  { "Int", "int" },
  { "Float", "float" },
  { "Double", "double" },
  { "Const", "const" },
  { "Auto", "auto" },

  { "If", "if" },
  { "Else", "else" },
  { "While", "while" },
  { "For", "for" },
  { "Do", "do" },
  { "Break", "break" },
  { "Continue", "continue" },
  { "Return", "return" },

  { "Identifier", "identifier" },

  { "LeftParen", "l_paren" },
  { "RightParen", "r_paren" },
  { "RightBrace", "r_brace" },
  { "LeftBrace", "l_brace" },
  { "LeftBracket", "l_square" },
  { "RightBracket", "r_square" },

  { "Constant", "numeric_constant" },

  { "Plus", "plus" },
  { "Minus", "minus" },
  { "Star", "star" },
  { "Slash", "slash" },
  { "Percent", "percent" },
  { "Exclaim", "exclaim" },
  { "Amp", "amp" },
  { "Pipe", "pipe" },

  { "PlusEqual", "plusequal" },
  { "MinusEqual", "minusequal" },
  { "StarEqual", "starequal" },
  { "SlashEqual", "slashequal" },
  { "PercentEqual", "percentequal" },
  { "ExclaimEqual", "exclaimequal" },

  { "AmpAmp", "ampamp" },
  { "PipePipe", "pipepipe" },

  { "Less", "less" },
  { "Greater", "greater" },
  { "LessEqual", "lessequal" },
  { "GreaterEqual", "greaterequal" },
  { "EqualEqual", "equalequal" },

  { "Semi", "semi" },
  { "Comma", "comma" },

  { "Equal", "equal" },

  { "EOF", "eof" },
  // 在这里继续添加其他映射
};

void
print_token(const antlr4::Token* token,
            const antlr4::CommonTokenStream& tokens,
            std::ofstream& outFile,
            const antlr4::Lexer& lexer)
{
  auto& vocabulary = lexer.getVocabulary();

  auto tokenTypeName =
    std::string(vocabulary.getSymbolicName(token->getType()));

  if (tokenTypeName.empty())
    tokenTypeName = "<UNKNOWN>"; // 处理可能的空字符串情况

  if (tokenTypeName == "LineAfterPreprocessing" ||
      tokenTypeName == "Whitespace" ||
      tokenTypeName == "Newline") {
    return;
  }
  if (tokenTypeMapping.find(tokenTypeName) != tokenTypeMapping.end()) {
    tokenTypeName = tokenTypeMapping[tokenTypeName];
  }

  size_t tokenLine = token->getLine();
  size_t tokenIndex = token->getTokenIndex();

  // build locInfo
  std::string filename = "";
  for (size_t i = tokenIndex - 1; ; i--) {
    const antlr4::Token* t = tokens.get(i);
    std::string tokenTypeName = std::string(vocabulary.getSymbolicName(t->getType()));
    if (tokenTypeName == "LineAfterPreprocessing") {
      std::regex pattern("# (\\d+) \"([^\"]+)\"");
      std::smatch match;
      std::string text = t->getText();
      if (std::regex_search(text, match, pattern)) {
        size_t actualLine = std::stoi(match[1].str());
        tokenLine = actualLine + tokenLine - t->getLine() - 1;
        filename = match[2].str();
        break;
      }
    }
  }

  std::string locInfo = " Loc=<0:0>";
  if (filename.empty()) {
    locInfo = " Loc=<" + std::to_string(tokenLine) + ":" +
              std::to_string(token->getCharPositionInLine() + 1) + ">";
  } else {
    locInfo = " Loc=<" + filename + ":" + 
              std::to_string(tokenLine) + ":" +
              std::to_string(token->getCharPositionInLine() + 1) + ">";
  }

  bool startOfLine = false;
  bool leadingSpace = false;

  if (tokenIndex == 0) {
    startOfLine = true;
  } 
  else {
    const antlr4::Token* prevToken = tokens.get(tokenIndex - 1);
    if (token->getLine() > prevToken->getLine()) {
      startOfLine = true;
    }
  }

  if (startOfLine) {
    if (token->getCharPositionInLine() > 0) {
      leadingSpace = true;
    }
  }
  else {
    const antlr4::Token* prevToken = tokens.get(tokenIndex - 1);
    if (token->getCharPositionInLine() > prevToken->getCharPositionInLine() + prevToken->getText().length()) {
      leadingSpace = true;
    }
  }

  if (token->getText() != "<EOF>")
    outFile << tokenTypeName << " '" << token->getText() << "'";
  else
    outFile << tokenTypeName << " '"
            << "'";
  if (startOfLine)
    outFile << "\t [StartOfLine]";
  if (leadingSpace)
    outFile << " [LeadingSpace]";
  outFile << locInfo << std::endl;
}

int
main(int argc, char* argv[])
{
  if (argc != 3) {
    std::cout << "Usage: " << argv[0] << " <input> <output>\n";
    return -1;
  }

  std::ifstream inFile(argv[1]);
  if (!inFile) {
    std::cout << "Error: unable to open input file: " << argv[1] << '\n';
    return -2;
  }

  std::ofstream outFile(argv[2]);
  if (!outFile) {
    std::cout << "Error: unable to open output file: " << argv[2] << '\n';
    return -3;
  }

  std::cout << "程序 '" << argv[0] << std::endl;
  std::cout << "输入 '" << argv[1] << std::endl;
  std::cout << "输出 '" << argv[2] << std::endl;

  antlr4::ANTLRInputStream input(inFile);
  SYsULexer lexer(&input);

  antlr4::CommonTokenStream tokens(&lexer);
  tokens.fill();

  for (auto&& token : tokens.getTokens()) {
    print_token(token, tokens, outFile, lexer);
  }
}
