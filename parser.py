from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ASTNode:
    node_type: str
    value:     Any            = None
    line:      int            = 0
    column:    int            = 0
    children:  List[ASTNode] = field(default_factory=list)

    def __repr__(self) -> str:
        return self._fmt(0)

    def _fmt(self, depth: int) -> str:
        pad = "  " * depth
        hdr = f"{pad}[{self.node_type}]"
        if self.value is not None:
            hdr += f"  ← {self.value!r}"
        if self.line:
            hdr += f"  (line {self.line})"
        lines = [hdr]
        for ch in self.children:
            if isinstance(ch, ASTNode):
                lines.append(ch._fmt(depth + 1))
            else:
                lines.append(f"{'  '*(depth+1)}{ch!r}")
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        return {
            "node_type": self.node_type,
            "value":     self.value,
            "line":      self.line,
            "column":    self.column,
            "children":  [c.to_dict() if isinstance(c, ASTNode)
                          else c for c in self.children],
        }


@dataclass
class ParseError:
    message: str
    line:    int
    column:  int

    def __str__(self) -> str:
        return f"[Line {self.line}, Col {self.column}] SyntaxError: {self.message}"

    def to_dict(self) -> Dict:
        return {"message": self.message, "line": self.line, "column": self.column}


class Parser:

    _TYPE_TOKENS = frozenset({
        'KEYWORD_INT',    'KEYWORD_FLOAT',  'KEYWORD_CHAR',
        'KEYWORD_DOUBLE', 'KEYWORD_VOID',   'KEYWORD_STRING',
        'KEYWORD_LONG',   'KEYWORD_LONG_DOUBLE',
    })

    _NUMBER_TOKENS = frozenset({'LITERAL_INTEGER', 'LITERAL_FLOAT'})

    _ADD_OPS = frozenset({'OPERATOR_PLUS', 'OPERATOR_MINUS'})
    _MUL_OPS = frozenset({'OPERATOR_MULT', 'OPERATOR_DIV'})

    _INC_DEC = frozenset({'OPERATOR_INCREMENT', 'OPERATOR_DECREMENT'})

    _FACTOR_FIRST = frozenset({
        'IDENTIFIER',      'LITERAL_INTEGER',    'LITERAL_FLOAT',
        'LITERAL_CHAR',    'LITERAL_STRING',
        'SEPARATOR_LPAREN','OPERATOR_MINUS',
        'OPERATOR_INCREMENT', 'OPERATOR_DECREMENT',
    })

    _STMT_FIRST = frozenset({
        'KEYWORD_INT',    'KEYWORD_FLOAT',  'KEYWORD_CHAR',
        'KEYWORD_DOUBLE', 'KEYWORD_VOID',   'KEYWORD_STRING',
        'KEYWORD_LONG',   'KEYWORD_LONG_DOUBLE',
        'KEYWORD_IF',     'KEYWORD_FOR',    'KEYWORD_WHILE',
        'KEYWORD_DO',     'KEYWORD_RETURN',
        'IDENTIFIER',
    })

    def __init__(self, tokens: List[Dict]):
        self._tokens: List[Dict] = [
            t for t in tokens if t.get('category') != 'COMMENT'
        ]
        self._pos:    int              = 0
        self._errors: List[ParseError] = []

    def getErrors(self) -> List[ParseError]:
        return list(self._errors)

    def hasErrors(self) -> bool:
        return bool(self._errors)

    def peek(self) -> Optional[Dict]:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _peek2(self) -> Optional[Dict]:
        idx = self._pos + 1
        return self._tokens[idx] if idx < len(self._tokens) else None

    def advance(self) -> Optional[Dict]:
        tok = self.peek()
        if tok is not None:
            self._pos += 1
        return tok

    def match(self, expected_type: str) -> Optional[Dict]:
        tok = self.peek()
        if tok is None:
            self._record_error(
                f"Expected '{expected_type}' but reached end of input"
            )
            return None
        if tok['type'] == expected_type:
            return self.advance()
        self._record_error(
            f"Expected '{expected_type}' "
            f"but got '{tok['type']}' ('{tok['value']}')",
            tok,
        )
        return None

    def _at_end(self) -> bool:
        return self._pos >= len(self._tokens)

    def _record_error(self, message: str, tok: Optional[Dict] = None) -> None:
        if tok is None:
            tok = self.peek()
        line   = tok['line']           if tok else 0
        column = tok.get('column', 0)  if tok else 0
        self._errors.append(ParseError(message, line, column))

    def _sync_to(self, *stop_types: str) -> None:
        while not self._at_end():
            if self.peek()['type'] in stop_types:
                break
            self.advance()

                                                                       
                   
                                                                       

    def parseProgram(self) -> ASTNode:
        node = ASTNode('Program', line=1)
        while not self._at_end():
            tok = self.peek()

                                                                       
            if self._isMainFunction():
                main_node = self.parseMainFunction()
                if main_node is not None:
                    node.children.append(main_node)
                continue

            stmt = self.parseStatement()
            if stmt is not None:
                node.children.append(stmt)
            else:
                if tok is not None:
                    self._record_error(
                        f"Unexpected token '{tok['value']}' "
                        f"(type '{tok['type']}') — skipping for recovery",
                        tok,
                    )
                    self.advance()
        return node

                                                                       
                    
                                                                       

    def _isMainFunction(self) -> bool:
        tok  = self.peek()
        tok2 = self._peek2()
        if tok is None or tok2 is None:
            return False
        if tok['type'] not in self._TYPE_TOKENS:
            return False
        if tok2['type'] != 'IDENTIFIER':
            return False
        if tok2['value'] != 'main':
            return False
        idx3 = self._pos + 2
        if idx3 >= len(self._tokens):
            return False
        return self._tokens[idx3]['type'] == 'SEPARATOR_LPAREN'

    def parseMainFunction(self) -> Optional[ASTNode]:
        ret_tok  = self.advance()
        name_tok = self.advance()
        self.match('SEPARATOR_LPAREN')
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        body = self._parseBlock()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('MainFunction',
                       value='main',
                       line=ret_tok['line'],
                       column=ret_tok.get('column', 0))
        node.children.append(
            ASTNode('ReturnType', value=ret_tok['value'],
                    line=ret_tok['line'])
        )
        node.children.append(
            ASTNode('Body', children=body, line=ret_tok['line'])
        )
        return node

                                                                       
                     
                                                                       

    def parseStatement(self) -> Optional[ASTNode]:
        tok = self.peek()
        if tok is None:
            return None

        tt = tok['type']

        if tt in self._TYPE_TOKENS:
            return self._parseDeclarationOrInit()

        if tt == 'KEYWORD_IF':
            return self.parseIfStatement()

        if tt == 'KEYWORD_FOR':
            return self.parseForLoop()

        if tt == 'KEYWORD_WHILE':
            return self.parseWhileLoop()

        if tt == 'KEYWORD_DO':
            return self.parseDoWhileLoop()

        if tt == 'KEYWORD_RETURN':
            return self.parseReturnStatement()

        if tt == 'IDENTIFIER':
            nxt = self._peek2()
            if nxt and nxt['type'] == 'OPERATOR_ASSIGN':
                return self.parseAssignment()
            if nxt and nxt['type'] in self._INC_DEC:
                return self.parsePostfixStatement()
            self._record_error(
                f"Expected '=' after identifier '{tok['value']}' for assignment",
                nxt or tok,
            )
            return self.parseAssignment()

        if tt in self._INC_DEC:
            return self.parsePrefixStatement()

        return None

                                                                       
                                      
                                     
                                        
                                                                       

    def _parseDeclarationOrInit(self) -> Optional[ASTNode]:
        type_node = self.parseType()
        if type_node is None:
            return None

        id_tok = self.match('IDENTIFIER')
        if id_tok is None:
            self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            if not self._at_end() and\
                    self.peek()['type'] == 'SEPARATOR_SEMICOLON':
                self.advance()
            return None

        nxt = self.peek()

                                                                      
        if nxt and nxt['type'] == 'OPERATOR_ASSIGN':
            self.advance()
            expr = self.parseExpression()
            if expr is None:
                self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            semi = self.match('SEPARATOR_SEMICOLON')
            if semi is None:
                self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
                if not self._at_end() and\
                        self.peek()['type'] == 'SEPARATOR_SEMICOLON':
                    self.advance()
            node = ASTNode('Initialization',
                           line=type_node.line, column=type_node.column)
            node.children.append(type_node)
            node.children.append(
                ASTNode('Identifier', value=id_tok['value'],
                        line=id_tok['line'], column=id_tok.get('column', 0))
            )
            if expr:
                node.children.append(expr)
            return node

                                                                       
        semi = self.match('SEPARATOR_SEMICOLON')
        if semi is None:
            self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            if not self._at_end() and\
                    self.peek()['type'] == 'SEPARATOR_SEMICOLON':
                self.advance()

        node = ASTNode('Declaration',
                       line=type_node.line, column=type_node.column)
        node.children.append(type_node)
        node.children.append(
            ASTNode('Identifier', value=id_tok['value'],
                    line=id_tok['line'], column=id_tok.get('column', 0))
        )
        return node

    def parseDeclaration(self) -> Optional[ASTNode]:
        return self._parseDeclarationOrInit()

                                                                       
                      
                                                                       

    def parseAssignment(self) -> Optional[ASTNode]:
        id_tok = self.match('IDENTIFIER')
        if id_tok is None:
            self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            return None

        eq_tok = self.match('OPERATOR_ASSIGN')
        if eq_tok is None:
            self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            if not self._at_end() and\
                    self.peek()['type'] == 'SEPARATOR_SEMICOLON':
                self.advance()
            return None

        expr = self.parseExpression()
        if expr is None:
            self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')

        semi = self.match('SEPARATOR_SEMICOLON')
        if semi is None:
            self._sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            if not self._at_end() and\
                    self.peek()['type'] == 'SEPARATOR_SEMICOLON':
                self.advance()

        node = ASTNode('Assignment',
                       line=id_tok['line'], column=id_tok.get('column', 0))
        node.children.append(
            ASTNode('Identifier', value=id_tok['value'],
                    line=id_tok['line'], column=id_tok.get('column', 0))
        )
        if expr:
            node.children.append(expr)
        return node

                                                                       
                            
                                                                       

    def parsePostfixStatement(self) -> Optional[ASTNode]:
        id_tok = self.match('IDENTIFIER')
        op_tok = self.advance()
        self.match('SEPARATOR_SEMICOLON')
        node = ASTNode('PostfixOp', value=op_tok['value'],
                       line=id_tok['line'], column=id_tok.get('column', 0))
        node.children.append(
            ASTNode('Identifier', value=id_tok['value'],
                    line=id_tok['line'], column=id_tok.get('column', 0))
        )
        return node

                                                                       
                           
                                                                       

    def parsePrefixStatement(self) -> Optional[ASTNode]:
        op_tok = self.advance()
        id_tok = self.match('IDENTIFIER')
        self.match('SEPARATOR_SEMICOLON')
        node = ASTNode('PrefixOp', value=op_tok['value'],
                       line=op_tok['line'], column=op_tok.get('column', 0))
        if id_tok:
            node.children.append(
                ASTNode('Identifier', value=id_tok['value'],
                        line=id_tok['line'], column=id_tok.get('column', 0))
            )
        return node

                                                                       
                       
                                                                       

    def parseIfStatement(self) -> Optional[ASTNode]:
        if_tok = self.match('KEYWORD_IF')
        if if_tok is None:
            return None

        self.match('SEPARATOR_LPAREN')
        cond = self.parseExpression()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        then_stmts = self._parseBlock()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('IfStatement',
                       line=if_tok['line'], column=if_tok.get('column', 0))
        if cond:
            node.children.append(
                ASTNode('Condition', children=[cond], line=if_tok['line'])
            )
        node.children.append(
            ASTNode('Then', children=then_stmts, line=if_tok['line'])
        )

        nxt = self.peek()
        if nxt and nxt['type'] == 'KEYWORD_ELSE':
            else_tok = self.advance()
            self.match('SEPARATOR_LBRACE')
            else_stmts = self._parseBlock()
            self.match('SEPARATOR_RBRACE')
            node.node_type = 'IfElseStatement'
            node.children.append(
                ASTNode('Else', children=else_stmts, line=else_tok['line'])
            )

        return node

                                                                       
                   
                                                                       

    def parseForLoop(self) -> Optional[ASTNode]:
        for_tok = self.match('KEYWORD_FOR')
        if for_tok is None:
            return None

        self.match('SEPARATOR_LPAREN')
        init_node = self.parseStatement()
        cond_node = self.parseExpression()
        self.match('SEPARATOR_SEMICOLON')
        upd_node  = self.parseExpression()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        body = self._parseBlock()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('ForLoop',
                       line=for_tok['line'], column=for_tok.get('column', 0))
        node.children.append(
            ASTNode('Init',
                    children=[init_node] if init_node else [],
                    line=for_tok['line'])
        )
        node.children.append(
            ASTNode('Condition',
                    children=[cond_node] if cond_node else [],
                    line=for_tok['line'])
        )
        node.children.append(
            ASTNode('Update',
                    children=[upd_node] if upd_node else [],
                    line=for_tok['line'])
        )
        node.children.append(
            ASTNode('Body', children=body, line=for_tok['line'])
        )
        return node

                                                                       
                     
                                                                       

    def parseWhileLoop(self) -> Optional[ASTNode]:
        while_tok = self.match('KEYWORD_WHILE')
        if while_tok is None:
            return None

        self.match('SEPARATOR_LPAREN')
        cond = self.parseExpression()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        body = self._parseBlock()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('WhileLoop',
                       line=while_tok['line'], column=while_tok.get('column', 0))
        if cond:
            node.children.append(
                ASTNode('Condition', children=[cond], line=while_tok['line'])
            )
        node.children.append(
            ASTNode('Body', children=body, line=while_tok['line'])
        )
        return node

                                                                       
                               
                               
                                                                       

    def parseDoWhileLoop(self) -> Optional[ASTNode]:
        do_tok = self.match('KEYWORD_DO')
        if do_tok is None:
            return None

        self.match('SEPARATOR_LBRACE')
        body = self._parseBlock()
        self.match('SEPARATOR_RBRACE')
        self.match('KEYWORD_WHILE')
        self.match('SEPARATOR_LPAREN')
        cond = self.parseExpression()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_SEMICOLON')

        node = ASTNode('DoWhileLoop',
                       line=do_tok['line'], column=do_tok.get('column', 0))
        node.children.append(
            ASTNode('Body', children=body, line=do_tok['line'])
        )
        if cond:
            node.children.append(
                ASTNode('Condition', children=[cond], line=do_tok['line'])
            )
        return node

                                                                       
                                   
                                  
                                                                       

    def parseReturnStatement(self) -> Optional[ASTNode]:
        ret_tok = self.match('KEYWORD_RETURN')
        if ret_tok is None:
            return None

        node = ASTNode('ReturnStatement',
                       line=ret_tok['line'], column=ret_tok.get('column', 0))

        nxt = self.peek()
        if nxt and nxt['type'] != 'SEPARATOR_SEMICOLON':
            expr = self.parseExpression()
            if expr:
                node.children.append(expr)

        self.match('SEPARATOR_SEMICOLON')
        return node

                                                                       
                      
                                                                       

    def parseExpression(self) -> Optional[ASTNode]:
        left = self.parseTerm()
        if left is None:
            return None

        while True:
            tok = self.peek()
            if tok is None or tok['type'] not in self._ADD_OPS:
                break
            op    = self.advance()
            right = self.parseTerm()
            if right is None:
                self._record_error(
                    f"Missing right operand after '{op['value']}'", op
                )
                break
            parent = ASTNode('BinaryOp', value=op['value'],
                             line=op['line'], column=op.get('column', 0))
            parent.children.append(left)
            parent.children.append(right)
            left = parent

        return left

                                                                       
                
                                                                       

    def parseTerm(self) -> Optional[ASTNode]:
        left = self.parseFactor()
        if left is None:
            return None

        while True:
            tok = self.peek()
            if tok is None or tok['type'] not in self._MUL_OPS:
                break
            op    = self.advance()
            right = self.parseFactor()
            if right is None:
                self._record_error(
                    f"Missing right operand after '{op['value']}'", op
                )
                break
            parent = ASTNode('BinaryOp', value=op['value'],
                             line=op['line'], column=op.get('column', 0))
            parent.children.append(left)
            parent.children.append(right)
            left = parent

        return left

                                                                       
                                                                
                                                                       

    def parseFactor(self) -> Optional[ASTNode]:
        tok = self.peek()
        if tok is None:
            self._record_error(
                "Expected a value or expression but reached end of input"
            )
            return None

        tt = tok['type']

        if tt == 'SEPARATOR_LPAREN':
            self.advance()
            expr  = self.parseExpression()
            close = self.match('SEPARATOR_RPAREN')
            if close is None:
                self._sync_to(
                    'SEPARATOR_RPAREN', 'SEPARATOR_SEMICOLON',
                    'SEPARATOR_RBRACE'
                )
                if not self._at_end() and\
                        self.peek()['type'] == 'SEPARATOR_RPAREN':
                    self.advance()
            return expr

                                                                      
        if tt in self._INC_DEC:
            op      = self.advance()
            operand = self.parseFactor()
            node    = ASTNode('PrefixOp', value=op['value'],
                              line=op['line'], column=op.get('column', 0))
            if operand:
                node.children.append(operand)
            return node

        if tt == 'IDENTIFIER':
            self.advance()
            id_node = ASTNode('Identifier', value=tok['value'],
                              line=tok['line'], column=tok.get('column', 0))
                                                                      
            nxt = self.peek()
            if nxt and nxt['type'] in self._INC_DEC:
                op = self.advance()
                post = ASTNode('PostfixOp', value=op['value'],
                               line=op['line'], column=op.get('column', 0))
                post.children.append(id_node)
                return post
            return id_node

        if tt in self._NUMBER_TOKENS:
            self.advance()
            return ASTNode('Number', value=tok['value'],
                           line=tok['line'], column=tok.get('column', 0))

        if tt in ('LITERAL_CHAR', 'LITERAL_STRING'):
            self.advance()
            return ASTNode('Literal', value=tok['value'],
                           line=tok['line'], column=tok.get('column', 0))

        if tt == 'OPERATOR_MINUS':
            op      = self.advance()
            operand = self.parseFactor()
            node    = ASTNode('UnaryOp', value='-',
                              line=op['line'], column=op.get('column', 0))
            if operand:
                node.children.append(operand)
            return node

        self._record_error(
            f"Unexpected token '{tok['value']}' "
            f"(type '{tt}') in expression",
            tok,
        )
        return None

                                                                       
                                                              
                                                                       

    def parseType(self) -> Optional[ASTNode]:
        tok = self.peek()
        if tok is None:
            self._record_error(
                "Expected a type keyword but reached end of input"
            )
            return None

        if tok['type'] in self._TYPE_TOKENS:
            self.advance()
            return ASTNode('Type', value=tok['value'],
                           line=tok['line'], column=tok.get('column', 0))

        self._record_error(
            f"Expected a type keyword "
            f"(int / float / char / double / void / string / long) "
            f"but got '{tok['value']}'",
            tok,
        )
        return None

                                                                       
                  
                                                                       

    def _parseBlock(self) -> List[ASTNode]:
        stmts: List[ASTNode] = []
        while not self._at_end():
            tok = self.peek()
            if tok['type'] == 'SEPARATOR_RBRACE':
                break
            stmt = self.parseStatement()
            if stmt is not None:
                stmts.append(stmt)
            else:
                bad = self.peek()
                if bad and bad['type'] != 'SEPARATOR_RBRACE':
                    self._record_error(
                        f"Unexpected token '{bad['value']}' "
                        f"inside block — skipping for recovery",
                        bad,
                    )
                    self.advance()
                else:
                    break
        return stmts


                                                                               
                      
                                                                               

def parse(tokens: List[Dict]) -> tuple[ASTNode, List[ParseError]]:
    p   = Parser(tokens)
    ast = p.parseProgram()
    return ast, p.getErrors()


                                                                               
      
                                                                               

if __name__ == '__main__':
    import sys
    import os

    try:
        _dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, _dir)
        from app import tokenize
        _HAS_TOKENIZER = True
    except ImportError:
        _HAS_TOKENIZER = False

    def _sep(char: str = '─', width: int = 70) -> str:
        return char * width

    if len(sys.argv) >= 2:
        src_path = sys.argv[1]
        try:
            with open(src_path, 'r', encoding='utf-8') as fh:
                source = fh.read()
        except FileNotFoundError:
            print(f"[Error] File not found: {src_path}")
            sys.exit(1)
    else:
        source = """\
int main() {
    int x;
    float result;
    int y = 10;
    char c = 'a';
    long n = 100;
    x = y * 2 + 5;

    if (x) {
        int a = 1;
        a++;
        ++a;
    } else {
        int b = 2;
        b--;
    }

    while (x) {
        x = x - 1;
        x--;
    }

    do {
        y = y + 1;
    } while (y);

    for (int i = 0; i; i + 1) {
        result = result + i;
    }

    return 0;
}
"""
        print("[Info] No file supplied — running built-in demo source.\n")

    if _HAS_TOKENIZER:
        tokens = tokenize(source)
    else:
        print("[Warning] app.py not found — using minimal built-in tokenizer.\n")
        import re as _re

        _KW = {
            'int':    'KEYWORD_INT',    'float':  'KEYWORD_FLOAT',
            'char':   'KEYWORD_CHAR',   'double': 'KEYWORD_DOUBLE',
            'void':   'KEYWORD_VOID',   'string': 'KEYWORD_STRING',
            'long':   'KEYWORD_LONG',
            'if':     'KEYWORD_IF',     'else':   'KEYWORD_ELSE',
            'while':  'KEYWORD_WHILE',  'for':    'KEYWORD_FOR',
            'do':     'KEYWORD_DO',     'return': 'KEYWORD_RETURN',
            'main':   'IDENTIFIER',
        }
        _OP2 = {
            '++': 'OPERATOR_INCREMENT', '--': 'OPERATOR_DECREMENT',
            '==': 'OPERATOR_EQ',        '!=': 'OPERATOR_NEQ',
            '<=': 'OPERATOR_LTE',       '>=': 'OPERATOR_GTE',
        }
        _OP1 = {
            '=': 'OPERATOR_ASSIGN', '+': 'OPERATOR_PLUS',
            '-': 'OPERATOR_MINUS',  '*': 'OPERATOR_MULT',
            '/': 'OPERATOR_DIV',
        }
        _SEP = {
            '(': 'SEPARATOR_LPAREN',  ')': 'SEPARATOR_RPAREN',
            '{': 'SEPARATOR_LBRACE',  '}': 'SEPARATOR_RBRACE',
            ';': 'SEPARATOR_SEMICOLON', ',': 'SEPARATOR_COMMA',
        }
        _PAT = _re.compile(
            r'//[^\n]*'
            r'|/\*.*?\*/'
            r"|'(?:[^'\\]|\\.)*'"
            r'|"(?:[^"\\]|\\.)*"'
            r'|(\d+\.\d+)|(\d+)'
            r'|(\+\+|--|==|!=|<=|>=)'
            r'|([=+\-*/])'
            r'|([;,(){}])'
            r'|([a-zA-Z_]\w*)'
            r'|(\s+)',
            _re.DOTALL,
        )
        tokens, line = [], 1
        for m in _PAT.finditer(source):
            full = m.group(0)
            if full.startswith('//') or full.startswith('/*'):
                line += full.count('\n')
                continue
            flt, num, op2, op1, sep, ident, ws = m.groups()
            if ws:
                line += ws.count('\n')
                continue
            col = m.start()
            if flt:
                tokens.append({'category': 'LITERAL',   'type': 'LITERAL_FLOAT',
                               'value': flt,  'line': line, 'column': col})
            elif num:
                tokens.append({'category': 'LITERAL',   'type': 'LITERAL_INTEGER',
                               'value': num,  'line': line, 'column': col})
            elif op2:
                tokens.append({'category': 'OPERATOR',  'type': _OP2[op2],
                               'value': op2,  'line': line, 'column': col})
            elif op1:
                tokens.append({'category': 'OPERATOR',  'type': _OP1[op1],
                               'value': op1,  'line': line, 'column': col})
            elif sep:
                tokens.append({'category': 'SEPARATOR', 'type': _SEP[sep],
                               'value': sep,  'line': line, 'column': col})
            elif ident:
                t   = _KW.get(ident, 'IDENTIFIER')
                cat = 'KEYWORD' if t.startswith('KEYWORD') else 'IDENTIFIER'
                tokens.append({'category': cat, 'type': t,
                               'value': ident, 'line': line, 'column': col})
            elif full.startswith("'") or full.startswith('"'):
                t = 'LITERAL_CHAR' if full.startswith("'") else 'LITERAL_STRING'
                tokens.append({'category': 'LITERAL', 'type': t,
                               'value': full, 'line': line, 'column': col})

    parser = Parser(tokens)
    ast    = parser.parseProgram()
    errors = parser.getErrors()

    print(_sep('═'))
    print("  W++ RECURSIVE DESCENT PARSER — OUTPUT")
    print(_sep('═'))

    print(f"\n  SYNTAX ERRORS")
    print(_sep())
    if errors:
        for i, err in enumerate(errors, 1):
            print(f"  {i:>2}. {err}")
    else:
        print("  ✓  No syntax errors found.")

    print(f"\n\n  ABSTRACT SYNTAX TREE (AST)")
    print(_sep())
    print(ast)

    print()
    print(_sep('═'))
    status = "FAILED" if errors else "PASSED"
    print(f"  Parse status: {status}  |  "
          f"{len(tokens)} tokens  |  "
          f"{len(errors)} error(s)")
    print(_sep('═'))
