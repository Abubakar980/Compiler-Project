from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


                                                               
             
                                                               

type_keywords = {
    'KEYWORD_INT',    'KEYWORD_FLOAT',  'KEYWORD_CHAR',
    'KEYWORD_DOUBLE', 'KEYWORD_VOID',   'KEYWORD_STRING',
    'KEYWORD_LONG',   'KEYWORD_BOOL',
}

add_operators = {
    'OPERATOR_PLUS',
    'OPERATOR_MINUS',
}

mul_operators = {
    'OPERATOR_MULT',
    'OPERATOR_DIV',
    'OPERATOR_MOD',
}

inc_dec_operators = {
    'OPERATOR_INCREMENT',
    'OPERATOR_DECREMENT',
}

compare_operators = {
    'OPERATOR_EQ',  'OPERATOR_NEQ',
    'OPERATOR_LT',  'OPERATOR_GT',
    'OPERATOR_LTE', 'OPERATOR_GTE',
}

logical_operators = {
    'OPERATOR_AND',
    'OPERATOR_OR',
}

number_literals = {
    'LITERAL_INTEGER',
    'LITERAL_FLOAT',
}

all_literals = {
    'LITERAL_INTEGER', 'LITERAL_FLOAT',
    'LITERAL_CHAR',    'LITERAL_STRING',
}


                                                               
           
                                                               

@dataclass
class ASTNode:
    node_type : str
    value     : Any           = None
    line      : int           = 0
    column    : int           = 0
    children  : List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return self._fmt(0)

    def _fmt(self, depth):
        pad  = '  ' * depth
        text = f'{pad}[{self.node_type}]'
        if self.value is not None:
            text += f'  <- {self.value!r}'
        if self.line:
            text += f'  (line {self.line}'
        rows = [text]
        for child in self.children:
            if isinstance(child, ASTNode):
                rows.append(child._fmt(depth + 1))
            else:
                rows.append(f'{"  "*(depth+1)}{child!r}')
        return '\n'.join(rows)

    def to_dict(self):
        return {
            'node_type' : self.node_type,
            'value'     : self.value,
            'line'      : self.line,
            'column'    : self.column,
            'children'  : [
                c.to_dict() if isinstance(c, ASTNode) else c
                for c in self.children
            ],
        }


                                                               
              
                                                               

@dataclass
class ParseError:
    message : str
    line    : int
    column  : int

    def __str__(self):
        return f'[Line {self.line}, Col {self.column}] SyntaxError: {self.message}'

    def to_dict(self):
        return {
            'message' : self.message,
            'line'    : self.line,
            'column'  : self.column,
        }


                                                               
         
                                                               

class Parser:

    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.get('category') != 'COMMENT']
        self.pos    = 0
        self.errors = []

                                                               
                 
                                                               

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def peek2(self):
        idx = self.pos + 1
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None

    def peek3(self):
        idx = self.pos + 2
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None

    def advance(self):
        tok = self.peek()
        if tok is not None:
            self.pos += 1
        return tok

    def at_end(self):
        return self.pos >= len(self.tokens)

                                                               
                    
                                                               

    def match(self, expected_type, error_tok=None):
        tok = self.peek()
        if tok is None:
            self.add_error(f"Expected '{expected_type}' but reached end of file")
            return None
        if tok['type'] == expected_type:
            return self.advance()
        # If caller gave a specific token for error location, use that line
        report_at = error_tok if error_tok is not None else tok
        if expected_type == 'SEPARATOR_SEMICOLON' and error_tok is not None:
            self.add_error("Missing ';' at end of statement", report_at)
        else:
            self.add_error(
                f"Expected '{expected_type}' but got '{tok['value']}'", report_at
            )
        return None

    def add_error(self, message, tok=None):
        if tok is None:
            tok = self.peek()
        line   = tok['line']          if tok else 0
        column = tok.get('column', 0) if tok else 0
        self.errors.append(ParseError(message, line, column))

    def sync_to(self, *stop_types):
        while not self.at_end():
            if self.peek()['type'] in stop_types:
                break
            self.advance()

                                                               
             
                                                               

    def getErrors(self):
        return list(self.errors)

    def hasErrors(self):
        return bool(self.errors)

                                                               
              
                                                               

    def parseProgram(self):
        program = ASTNode('Program', line=1)

        while not self.at_end():
            tok = self.peek()

            if self.is_main_function():
                node = self.parseMainFunction()
            else:
                node = self.parseStatement()

            if node is not None:
                program.children.append(node)
            else:
                if tok is not None:
                    self.add_error(
                        f"Unexpected token '{tok['value']}' — skipped", tok
                    )
                    self.advance()

        return program

                                                               
                    
                                                               

    def is_main_function(self):
        t1 = self.peek()
        t2 = self.peek2()
        t3 = self.peek3()
        if t1 is None or t2 is None or t3 is None:
            return False
        return (
            t1['type'] in type_keywords
            and t2['type'] == 'IDENTIFIER'
            and t2['value'] == 'main'
            and t3['type'] == 'SEPARATOR_LPAREN'
        )

    def parseMainFunction(self):
        ret_tok = self.advance()
        self.advance()
        self.match('SEPARATOR_LPAREN')
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        body = self.parse_block()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('MainFunction', value='main',
                       line=ret_tok['line'], column=ret_tok.get('column', 0))
        node.children.append(
            ASTNode('ReturnType', value=ret_tok['value'], line=ret_tok['line'])
        )
        node.children.append(
            ASTNode('Body', children=body, line=ret_tok['line'])
        )
        return node

                                                               
                
                                                               

    def parseStatement(self):
        tok = self.peek()
        if tok is None:
            return None

        tt = tok['type']

        if tt in type_keywords:
            return self.parseDeclarationOrInit()

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

        if tt == 'KEYWORD_PRINT':
            return self.parsePrint()

        if tt == 'KEYWORD_READ':
            return self.parseRead()

        if tt == 'IDENTIFIER':
            nxt = self.peek2()
            if nxt and nxt['type'] == 'OPERATOR_ASSIGN':
                return self.parseAssignment()
            if nxt and nxt['type'] in inc_dec_operators:
                return self.parsePostfix()
            self.add_error(
                f"Expected '=' after '{tok['value']}'", nxt or tok
            )
            return self.parseAssignment()

        if tt in inc_dec_operators:
            return self.parsePrefix()

        return None

                                                               
                               
                                    
                                                               

    def _parseForUpdate(self):
        tok = self.peek()
        if tok is None:
            return None
        nxt = self.peek2()
        if tok['type'] == 'IDENTIFIER' and nxt and nxt['type'] == 'OPERATOR_ASSIGN':
            id_tok = self.advance()
            self.advance()
            expr = self.parseExpression()
            node = ASTNode('Assignment',
                           line=id_tok['line'], column=id_tok.get('column', 0))
            node.children.append(
                ASTNode('Identifier', value=id_tok['value'],
                        line=id_tok['line'], column=id_tok.get('column', 0))
            )
            if expr:
                node.children.append(expr)
            return node
        if tok['type'] == 'IDENTIFIER' and nxt and nxt['type'] in inc_dec_operators:
            id_tok = self.advance()
            op_tok = self.advance()
            node = ASTNode('PostfixOp', value=op_tok['value'],
                           line=id_tok['line'], column=id_tok.get('column', 0))
            node.children.append(
                ASTNode('Identifier', value=id_tok['value'],
                        line=id_tok['line'], column=id_tok.get('column', 0))
            )
            return node
        if tok['type'] in inc_dec_operators:
            op_tok = self.advance()
            id_tok = self.match('IDENTIFIER')
            node = ASTNode('PrefixOp', value=op_tok['value'],
                           line=op_tok['line'], column=op_tok.get('column', 0))
            if id_tok:
                node.children.append(
                    ASTNode('Identifier', value=id_tok['value'],
                            line=id_tok['line'], column=id_tok.get('column', 0))
                )
            return node
        return self.parseExpression()

    def parseDeclarationOrInit(self):
        type_node = self.parseType()
        if type_node is None:
            return None

        id_tok = self.match('IDENTIFIER')
        if id_tok is None:
            self.sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            if not self.at_end() and self.peek()['type'] == 'SEPARATOR_SEMICOLON':
                self.advance()
            return None

        nxt = self.peek()

        if nxt and nxt['type'] == 'OPERATOR_ASSIGN':
            self.advance()
            expr = self.parseExpression()
            if expr is None:
                self.sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')

            node = ASTNode('Initialization',
                           line=type_node.line, column=type_node.column)
            node.children.append(type_node)
            node.children.append(
                ASTNode('Identifier', value=id_tok['value'],
                        line=id_tok['line'], column=id_tok.get('column', 0))
            )
            if expr:
                node.children.append(expr)

            last_tok = id_tok
            while self.peek() and self.peek()['type'] == 'SEPARATOR_COMMA':
                self.advance()
                extra_id = self.match('IDENTIFIER')
                if extra_id is None:
                    break
                last_tok = extra_id
                extra_node = ASTNode('Initialization',
                                     line=type_node.line, column=type_node.column)
                extra_node.children.append(
                    ASTNode('Type', value=type_node.value, line=type_node.line)
                )
                extra_node.children.append(
                    ASTNode('Identifier', value=extra_id['value'],
                            line=extra_id['line'], column=extra_id.get('column', 0))
                )
                if self.peek() and self.peek()['type'] == 'OPERATOR_ASSIGN':
                    self.advance()
                    extra_expr = self.parseExpression()
                    if extra_expr:
                        extra_node.children.append(extra_expr)
                node.children.append(extra_node)

            self.match('SEPARATOR_SEMICOLON', error_tok=last_tok)
            return node

        node = ASTNode('Declaration',
                       line=type_node.line, column=type_node.column)
        node.children.append(type_node)
        node.children.append(
            ASTNode('Identifier', value=id_tok['value'],
                    line=id_tok['line'], column=id_tok.get('column', 0))
        )

        last_tok = id_tok
        while self.peek() and self.peek()['type'] == 'SEPARATOR_COMMA':
            self.advance()
            extra_id = self.match('IDENTIFIER')
            if extra_id is None:
                break
            last_tok = extra_id
            extra_node = ASTNode('Declaration',
                                 line=type_node.line, column=type_node.column)
            extra_node.children.append(
                ASTNode('Type', value=type_node.value, line=type_node.line)
            )
            extra_node.children.append(
                ASTNode('Identifier', value=extra_id['value'],
                        line=extra_id['line'], column=extra_id.get('column', 0))
            )
            if self.peek() and self.peek()['type'] == 'OPERATOR_ASSIGN':
                self.advance()
                extra_expr = self.parseExpression()
                if extra_expr:
                    extra_node.children.append(extra_expr)
            node.children.append(extra_node)

        self.match('SEPARATOR_SEMICOLON', error_tok=last_tok)
        return node

    def parseDeclaration(self):
        return self.parseDeclarationOrInit()

                                                               
                                 
                                                               

    def parseAssignment(self):
        id_tok = self.match('IDENTIFIER')
        if id_tok is None:
            self.sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            return None

        if self.match('OPERATOR_ASSIGN') is None:
            self.sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')
            if not self.at_end() and self.peek()['type'] == 'SEPARATOR_SEMICOLON':
                self.advance()
            return None

        expr = self.parseExpression()
        if expr is None:
            self.sync_to('SEPARATOR_SEMICOLON', 'SEPARATOR_RBRACE')

        self.match('SEPARATOR_SEMICOLON')

        node = ASTNode('Assignment',
                       line=id_tok['line'], column=id_tok.get('column', 0))
        node.children.append(
            ASTNode('Identifier', value=id_tok['value'],
                    line=id_tok['line'], column=id_tok.get('column', 0))
        )
        if expr:
            node.children.append(expr)
        return node

                                                               
                                
                                
                                                               

    def parsePostfix(self):
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

    def parsePrefix(self):
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

                                                               
                   
                                                               

    def parseIfStatement(self):
        if_tok = self.match('KEYWORD_IF')
        if if_tok is None:
            return None

        self.match('SEPARATOR_LPAREN')
        cond = self.parseExpression()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        then_body = self.parse_block()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('IfStatement',
                       line=if_tok['line'], column=if_tok.get('column', 0))
        if cond:
            node.children.append(
                ASTNode('Condition', children=[cond], line=if_tok['line'])
            )
        node.children.append(
            ASTNode('Then', children=then_body, line=if_tok['line'])
        )

        if self.peek() and self.peek()['type'] == 'KEYWORD_ELSE':
            else_tok = self.advance()
            if self.peek() and self.peek()['type'] == 'KEYWORD_IF':
                else_if_node = self.parseIfStatement()
                node.node_type = 'IfElseStatement'
                node.children.append(
                    ASTNode('Else', children=[else_if_node] if else_if_node else [], line=else_tok['line'])
                )
            else:
                self.match('SEPARATOR_LBRACE')
                else_body = self.parse_block()
                self.match('SEPARATOR_RBRACE')
                node.node_type = 'IfElseStatement'
                node.children.append(
                    ASTNode('Else', children=else_body, line=else_tok['line'])
                )

        return node

                                                               
               
                                                               

    def parseForLoop(self):
        for_tok = self.match('KEYWORD_FOR')
        if for_tok is None:
            return None

        self.match('SEPARATOR_LPAREN')
        init = self.parseStatement()
        cond = self.parseExpression()
        self.match('SEPARATOR_SEMICOLON')
        update = self._parseForUpdate()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        body = self.parse_block()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('ForLoop',
                       line=for_tok['line'], column=for_tok.get('column', 0))
        node.children.append(ASTNode('Init',      children=[init]   if init   else [], line=for_tok['line']))
        node.children.append(ASTNode('Condition', children=[cond]   if cond   else [], line=for_tok['line']))
        node.children.append(ASTNode('Update',    children=[update] if update else [], line=for_tok['line']))
        node.children.append(ASTNode('Body',      children=body,                       line=for_tok['line']))
        return node

                                                               
                 
                                                               

    def parseWhileLoop(self):
        while_tok = self.match('KEYWORD_WHILE')
        if while_tok is None:
            return None

        self.match('SEPARATOR_LPAREN')
        cond = self.parseExpression()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_LBRACE')
        body = self.parse_block()
        self.match('SEPARATOR_RBRACE')

        node = ASTNode('WhileLoop',
                       line=while_tok['line'], column=while_tok.get('column', 0))
        if cond:
            node.children.append(
                ASTNode('Condition', children=[cond], line=while_tok['line'])
            )
        node.children.append(ASTNode('Body', children=body, line=while_tok['line']))
        return node

                                                               
                    
                                                               

    def parseDoWhileLoop(self):
        do_tok = self.match('KEYWORD_DO')
        if do_tok is None:
            return None

        self.match('SEPARATOR_LBRACE')
        body = self.parse_block()
        self.match('SEPARATOR_RBRACE')
        self.match('KEYWORD_WHILE')
        self.match('SEPARATOR_LPAREN')
        cond = self.parseExpression()
        self.match('SEPARATOR_RPAREN')
        self.match('SEPARATOR_SEMICOLON')

        node = ASTNode('DoWhileLoop',
                       line=do_tok['line'], column=do_tok.get('column', 0))
        node.children.append(ASTNode('Body',      children=body,   line=do_tok['line']))
        if cond:
            node.children.append(ASTNode('Condition', children=[cond], line=do_tok['line']))
        return node

                                                               
             
                                                               

    def parseReturnStatement(self):
        ret_tok = self.match('KEYWORD_RETURN')
        if ret_tok is None:
            return None

        node = ASTNode('ReturnStatement',
                       line=ret_tok['line'], column=ret_tok.get('column', 0))

        if self.peek() and self.peek()['type'] != 'SEPARATOR_SEMICOLON':
            expr = self.parseExpression()
            if expr:
                node.children.append(expr)

        self.match('SEPARATOR_SEMICOLON')
        return node

    def parsePrint(self):
        print_tok = self.match('KEYWORD_PRINT')
        if print_tok is None:
            return None
        node = ASTNode('PrintStatement',
                       line=print_tok['line'], column=print_tok.get('column', 0))
        if self.peek() and self.peek()['type'] != 'SEPARATOR_SEMICOLON':
            expr = self.parseExpression()
            if expr:
                node.children.append(expr)
        self.match('SEPARATOR_SEMICOLON')
        return node

    def parseRead(self):
        read_tok = self.match('KEYWORD_READ')
        if read_tok is None:
            return None
        node = ASTNode('ReadStatement',
                       line=read_tok['line'], column=read_tok.get('column', 0))
        if self.peek() and self.peek()['type'] != 'SEPARATOR_SEMICOLON':
            expr = self.parseExpression()
            if expr:
                node.children.append(expr)
        self.match('SEPARATOR_SEMICOLON')
        return node

                                                               
                                                                      
                                                               

    def parseExpression(self):
        left = self.parse_comparison()
        if left is None:
            return None
        while self.peek() and self.peek()['type'] in logical_operators:
            op    = self.advance()
            right = self.parse_comparison()
            if right is None:
                self.add_error(f"Missing operand after '{op['value']}'", op)
                break
            parent = ASTNode('LogicalOp', value=op['value'],
                             line=op['line'], column=op.get('column', 0))
            parent.children.append(left)
            parent.children.append(right)
            left = parent
        return left

    def parse_comparison(self):
        left = self.parse_add_sub()
        if left is None:
            return None
        if self.peek() and self.peek()['type'] in compare_operators:
            op    = self.advance()
            right = self.parse_add_sub()
            if right is None:
                self.add_error(f"Missing operand after '{op['value']}'", op)
                return left
            parent = ASTNode('CompareOp', value=op['value'],
                             line=op['line'], column=op.get('column', 0))
            parent.children.append(left)
            parent.children.append(right)
            return parent
        return left

    def parse_add_sub(self):
        left = self.parseTerm()
        if left is None:
            return None
        while self.peek() and self.peek()['type'] in add_operators:
            op    = self.advance()
            right = self.parseTerm()
            if right is None:
                self.add_error(f"Missing operand after '{op['value']}'", op)
                break
            parent = ASTNode('BinaryOp', value=op['value'],
                             line=op['line'], column=op.get('column', 0))
            parent.children.append(left)
            parent.children.append(right)
            left = parent
        return left

    def parseTerm(self):
        left = self.parseFactor()
        if left is None:
            return None
        while self.peek() and self.peek()['type'] in mul_operators:
            op    = self.advance()
            right = self.parseFactor()
            if right is None:
                self.add_error(f"Missing operand after '{op['value']}'", op)
                break
            parent = ASTNode('BinaryOp', value=op['value'],
                             line=op['line'], column=op.get('column', 0))
            parent.children.append(left)
            parent.children.append(right)
            left = parent
        return left

    def parseFactor(self):
        tok = self.peek()
        if tok is None:
            self.add_error("Expected a value but reached end of file")
            return None

        tt = tok['type']

        if tt == 'SEPARATOR_LPAREN':
            self.advance()
            expr = self.parseExpression()
            self.match('SEPARATOR_RPAREN')
            return expr

        if tt in inc_dec_operators:
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
            if self.peek() and self.peek()['type'] in inc_dec_operators:
                op   = self.advance()
                post = ASTNode('PostfixOp', value=op['value'],
                               line=op['line'], column=op.get('column', 0))
                post.children.append(id_node)
                return post
            return id_node

        if tt in all_literals:
            self.advance()
            kind = 'Number' if tt in number_literals else 'Literal'
            return ASTNode(kind, value=tok['value'],
                           line=tok['line'], column=tok.get('column', 0))

        if tt == 'OPERATOR_MINUS':
            op      = self.advance()
            operand = self.parseFactor()
            node    = ASTNode('UnaryOp', value='-',
                              line=op['line'], column=op.get('column', 0))
            if operand:
                node.children.append(operand)
            return node

        if tt == 'OPERATOR_NOT':
            op      = self.advance()
            operand = self.parseFactor()
            node    = ASTNode('UnaryOp', value='!',
                              line=op['line'], column=op.get('column', 0))
            if operand:
                node.children.append(operand)
            return node

        if tt in ('KEYWORD_TRUE', 'KEYWORD_FALSE'):
            self.advance()
            return ASTNode('Boolean', value=tok['value'],
                           line=tok['line'], column=tok.get('column', 0))

        self.add_error(f"Unexpected token '{tok['value']}' in expression", tok)
        return None

                                                               
           
                                                               

    def parseType(self):
        tok = self.peek()
        if tok is None:
            self.add_error("Expected a type keyword but reached end of file")
            return None
        if tok['type'] in type_keywords:
            self.advance()
            return ASTNode('Type', value=tok['value'],
                           line=tok['line'], column=tok.get('column', 0))
        self.add_error(
            f"Expected a type (int/float/char/double/void/string/bool/long) "
            f"but got '{tok['value']}'", tok
        )
        return None

                                                               
                                  
                                                               

    def parse_block(self):
        stmts = []
        while not self.at_end():
            if self.peek()['type'] == 'SEPARATOR_RBRACE':
                break
            stmt = self.parseStatement()
            if stmt is not None:
                stmts.append(stmt)
            else:
                bad = self.peek()
                if bad and bad['type'] != 'SEPARATOR_RBRACE':
                    self.add_error(
                        f"Unexpected token '{bad['value']}' inside block — skipped", bad
                    )
                    self.advance()
                else:
                    break
        return stmts


                                                               
                                       
                                                               

def parse(tokens):
    p   = Parser(tokens)
    ast = p.parseProgram()
    return ast, p.getErrors()



