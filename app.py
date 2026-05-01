from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
import re
import os

_BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(_BASE, 'templates'))

keywords_list = {
    'int'    : 'KEYWORD_INT',
    'float'  : 'KEYWORD_FLOAT',
    'double' : 'KEYWORD_DOUBLE',
    'char'   : 'KEYWORD_CHAR',
    'string' : 'KEYWORD_STRING',
    'bool'   : 'KEYWORD_BOOL',
    'if'     : 'KEYWORD_IF',
    'else'   : 'KEYWORD_ELSE',
    'while'  : 'KEYWORD_WHILE',
    'for'    : 'KEYWORD_FOR',
    'return' : 'KEYWORD_RETURN',
    'print'  : 'KEYWORD_PRINT',
    'read'   : 'KEYWORD_READ',
    'true'   : 'KEYWORD_TRUE',
    'false'  : 'KEYWORD_FALSE',
}
two_char_ops = {
    '==': 'OPERATOR_EQ',
    '!=': 'OPERATOR_NEQ',
    '<=': 'OPERATOR_LTE',
    '>=': 'OPERATOR_GTE',
    '&&': 'OPERATOR_AND',
    '||': 'OPERATOR_OR'
}

one_char_ops = {
    '=': 'OPERATOR_ASSIGN',
    '+': 'OPERATOR_PLUS',
    '-': 'OPERATOR_MINUS',
    '*': 'OPERATOR_MULT',
    '/': 'OPERATOR_DIV',
    '%': 'OPERATOR_MOD',
    '<': 'OPERATOR_LT',
    '>': 'OPERATOR_GT',
    '!': 'OPERATOR_NOT'
}

separators_list = {
    '(': 'SEPARATOR_LPAREN',
    ')': 'SEPARATOR_RPAREN',
    '{': 'SEPARATOR_LBRACE',
    '}': 'SEPARATOR_RBRACE',
    ';': 'SEPARATOR_SEMICOLON',
    ',': 'SEPARATOR_COMMA'
}

TOKEN_PATTERN = re.compile(
    r'(?P<COMMENT_ML>  /\*[\s\S]*?\*/          )|'
    r'(?P<COMMENT_SL>  //[^\n]*                )|'
    r'(?P<STRING>      "(?:\\.|[^"\\])*"        )|'
    r'(?P<CHAR>        \'(?:\\.|[^\\\'])?\'     )|'
    r'(?P<FLOAT>       \d+\.\d+                 )|'
    r'(?P<INTEGER>     \d+                      )|'
    r'(?P<OP2>         ==|!=|<=|>=|&&|\|\|      )|'
    r'(?P<OP1>         [=+\-*/%<>!]             )|'
    r'(?P<SEPARATOR>   [;,(){}\[\]]             )|'
    r'(?P<IDENTIFIER>  [a-zA-Z_]\w*             )|'
    r'(?P<SKIP>        [ \t\r\n]+               )|'
    r'(?P<UNKNOWN>     .                         )',
    re.VERBOSE
)


def tokenize(source_code):
    token_list = []
    line_num = 1
    for match in TOKEN_PATTERN.finditer(source_code):

        token_type  = match.lastgroup
        token_value = match.group()

        if token_type == 'SKIP':
            line_num += token_value.count('\n')
            continue

        if token_type == 'UNKNOWN':
            continue

        if token_type == 'COMMENT_SL':
            token_list.append({
                'category': 'COMMENT',
                'type':     'COMMENT_SINGLELINE',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'COMMENT_ML':
            token_list.append({
                'category': 'COMMENT',
                'type':     'COMMENT_MULTILINE',
                'value':    '/* multi-line comment */',
                'line':     line_num
            })
            line_num += token_value.count('\n')
            continue

        if token_type == 'STRING':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_STRING',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'CHAR':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_CHAR',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'FLOAT':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_FLOAT',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'INTEGER':
            token_list.append({
                'category': 'LITERAL',
                'type':     'LITERAL_INTEGER',
                'value':    token_value,
                'line':     line_num
            })
            continue

        if token_type == 'OP2':
            token_list.append({
                'category': 'OPERATOR',
                'type': two_char_ops.get(token_value, 'OPERATOR_UNKNOWN'),
                'value': token_value,
                'line':  line_num
            })
            continue

        if token_type == 'OP1':
            token_list.append({
                'category': 'OPERATOR',
                'type': one_char_ops.get(token_value, 'OPERATOR_UNKNOWN'),
                'value': token_value,
                'line':  line_num
            })
            continue

        if token_type == 'SEPARATOR':
            token_list.append({
                'category': 'SEPARATOR',
                'type': separators_list.get(token_value, 'SEPARATOR_UNKNOWN'),
                'value': token_value,
                'line':  line_num
            })
            continue

        if token_type == 'IDENTIFIER':
            if token_value in keywords_list:
                token_list.append({
                    'category': 'KEYWORD',
                    'type':     'KEYWORD_' + token_value.upper(),
                    'value':    token_value,
                    'line':     line_num
                })
            else:
                token_list.append({
                    'category': 'IDENTIFIER',
                    'type':     'IDENTIFIER',
                    'value':    token_value,
                    'line':     line_num
                })
            continue

    return token_list


def get_type_summary_data(all_tokens, category_name):
    type_data = {}
    for tok in all_tokens:
        if tok['category'] != category_name:
            continue
        t_type = tok['type']
        if t_type not in type_data:
            type_data[t_type] = {'type': t_type, 'count': 0, 'lines': set()}
        type_data[t_type]['count'] += 1
        type_data[t_type]['lines'].add(tok['line'])
    result = []
    for data in type_data.values():
        data['lines'] = ', '.join(str(l) for l in sorted(data['lines']))
        result.append(data)
    return sorted(result, key=lambda x: x['type'])


def get_category_data(all_tokens, category_name):
    token_summary = {}
    total_in_cat = 0
    for tok in all_tokens:
        if tok['category'] != category_name:
            continue
        total_in_cat += 1
        t_type = tok['type']
        t_val = tok['value']
        t_line = tok['line']
        
        # Unique key for type and value
        key = (t_type, t_val)
        if key not in token_summary:
            token_summary[key] = {
                'type': t_type,
                'value': t_val,
                'count': 0,
                'lines': set()
            }
        token_summary[key]['count'] += 1
        token_summary[key]['lines'].add(t_line)
        
    result = []
    for key, data in token_summary.items():
        data['lines'] = ', '.join(str(l) for l in sorted(data['lines']))
        result.append(data)
    
    return sorted(result, key=lambda x: -x['count'])


def get_part_b(all_tokens, source_lines):
    line_count = defaultdict(int)
    for tok in all_tokens:
        line_count[tok['line']] += 1

    result = []
    for ln, raw in enumerate(source_lines, 1):
        result.append({
            'line_no':  ln,
            'content':  raw.strip(),
            'count':    line_count.get(ln, 0),
            'is_empty': raw.strip() == ''
        })
    return result


def get_part_c(all_tokens):
    data = {}
    for tok in all_tokens:
        if tok['category'] != 'IDENTIFIER':
            continue
        name = tok['value']
        if name not in data:
            data[name] = {'name': name, 'count': 0, 'lines': set()}
        data[name]['count'] += 1
        data[name]['lines'].add(tok['line'])

    result = sorted(data.values(), key=lambda x: -x['count'])
    for r in result:
        r['lines'] = ', '.join(str(l) for l in sorted(r['lines']))
    return result


def get_part_d(all_tokens):

    data = {}

    for tok in all_tokens:

        if tok['category'] != 'LITERAL':
            continue

        key = (tok['value'], tok['type'])

        if key not in data:
            data[key] = {
                'value'    : tok['value'],
                'type'     : tok['type'],
                'count'    : 0,
                'line_list': []
            }

        data[key]['count'] += 1

        if tok['line'] not in data[key]['line_list']:
            data[key]['line_list'].append(tok['line'])

    type_order = {
        'LITERAL_INTEGER': 1,
        'LITERAL_FLOAT'  : 2,
        'LITERAL_CHAR'   : 3,
        'LITERAL_STRING' : 4
    }

    def sort_literals(x):
        order_number = type_order.get(x['type'], 9)
        return (order_number, -x['count'])

    result = list(data.values())
    result.sort(key=sort_literals)

    for r in result:
        r['line_list'].sort()
        r['lines']      = ', '.join(str(l) for l in r['line_list'])
        r['short_type'] = r['type'].replace('LITERAL_', '')

    return result


def get_part_e(all_tokens, source_lines):
    non_cmt     = [t for t in all_tokens if t['category'] != 'COMMENT']
    total       = len(non_cmt)
    code_lines  = [l for l in source_lines if l.strip()]
    empty_lines = len(source_lines) - len(code_lines)

    unique_types = len(set(t['type'] for t in non_cmt))

    type_count = defaultdict(int)
    for t in non_cmt:
        type_count[t['type']] += 1

    most_freq  = max(type_count, key=type_count.get) if type_count else '-'
    least_freq = min(type_count, key=type_count.get) if type_count else '-'
    avg_tokens = round(total / len(code_lines), 2) if code_lines else 0

    line_tok = defaultdict(int)
    for t in non_cmt:
        line_tok[t['line']] += 1

    max_count = max(line_tok.values()) if line_tok else 0
    min_count = min(line_tok.values()) if line_tok else 0
    max_lines = sorted([ln for ln, c in line_tok.items() if c == max_count])
    min_lines = sorted([ln for ln, c in line_tok.items() if c == min_count])

    cat_count = defaultdict(int)
    for t in non_cmt:
        cat_count[t['category']] += 1

    breakdown = []
    for cat in ['KEYWORD', 'IDENTIFIER', 'LITERAL', 'OPERATOR', 'SEPARATOR', 'COMMENT']:
        cnt = cat_count.get(cat, 0)
        pct = round(cnt / total * 100, 2) if total > 0 else 0
        breakdown.append({
            'category': cat,
            'count':    cnt,
            'percent':  str(pct) + '%',
            'pct_val':  pct
        })

    mf_pct = str(round(type_count.get(most_freq, 0) / total * 100, 2)) + '%' if total else '0%'
    lf_pct = str(round(type_count.get(least_freq, 0) / total * 100, 2)) + '%' if total else '0%'

    return {
        'total_tokens':     total,
        'unique_types':     unique_types,
        'total_lines':      len(source_lines),
        'code_lines':       len(code_lines),
        'empty_lines':      empty_lines,
        'most_freq':        most_freq,
        'most_freq_count':  type_count.get(most_freq, 0),
        'most_freq_pct':    mf_pct,
        'least_freq':       least_freq,
        'least_freq_count': type_count.get(least_freq, 0),
        'least_freq_pct':   lf_pct,
        'avg_tokens':       avg_tokens,
        'max_line_count':   max_count,
        'max_line_nos':     ', '.join(str(l) for l in max_lines),
        'min_line_count':   min_count,
        'min_line_nos':     ', '.join(str(l) for l in min_lines),
        'breakdown':        breakdown,
        'most_freq_pct_val':  round(type_count.get(most_freq, 0) / total * 100, 2) if total else 0,
        'least_freq_pct_val': round(type_count.get(least_freq, 0) / total * 100, 2) if total else 0,
    }


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/analyzer', methods=['GET', 'POST'])
def analyzer():
    if request.method == 'GET':
        error = request.args.get('error')
        return render_template('index.html', error=error)

    source   = ''
    filename = '(pasted code)'

    if 'wpp_file' in request.files and request.files['wpp_file'].filename != '':
        uploaded = request.files['wpp_file']
        try:
            source   = uploaded.read().decode('utf-8')
            filename = uploaded.filename
        except UnicodeDecodeError:
            return redirect(url_for('analyzer', error='Error: Please upload a valid text/code file. This file contains invalid characters (like a PDF or Word document).'))

    else:
        source = request.form.get('source_code', '')

    if source.strip() == '':
        return redirect(url_for('analyzer', error='No code found.'))

    all_tokens   = tokenize(source)
    source_lines = source.split('\n')
    non_cmt      = [t for t in all_tokens if t['category'] != 'COMMENT']
    total_toks   = len(non_cmt)

    return render_template('result.html',
        filename = filename,
        b_data   = get_part_b(all_tokens, source_lines),
        c_data   = get_part_c(all_tokens),
        d_data   = get_part_d(all_tokens),
        e_data   = get_part_e(all_tokens, source_lines),
        kw_data  = get_type_summary_data(all_tokens, 'KEYWORD'),
        id_data  = get_type_summary_data(all_tokens, 'IDENTIFIER'),
        lit_data = get_type_summary_data(all_tokens, 'LITERAL'),
        op_data  = get_type_summary_data(all_tokens, 'OPERATOR'),
        sep_data = get_type_summary_data(all_tokens, 'SEPARATOR'),
        cmt_data = get_type_summary_data(all_tokens, 'COMMENT'),
    )


# if __name__ == '__main__':
#     print("Server is working...")
#     print("open in browser: http://localhost:5000")
#     app.run(debug=True)