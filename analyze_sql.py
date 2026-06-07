from pathlib import Path
import re

text = Path('database/churnhunters (2).sql').read_text(errors='ignore')
print('TOTAL_LINES', len(text.splitlines()))
for m in re.finditer(r"CREATE TABLE `([^`]+)`\s*\((.*?)\)\s*ENGINE=", text, re.S):
    table = m.group(1)
    body = m.group(2)
    cols = []
    for line in body.splitlines():
        s = line.strip().strip(',')
        if not s or s.startswith('PRIMARY KEY') or s.startswith('KEY ') or s.startswith('UNIQUE KEY') or s.startswith('CONSTRAINT') or s.startswith('FOREIGN KEY'):
            continue
        cols.append(s)
    print('\nTABLE', table, 'COLS', len(cols))
    for c in cols[:12]:
        print(' ', c)
    if len(cols) > 12:
        print('  ...')
