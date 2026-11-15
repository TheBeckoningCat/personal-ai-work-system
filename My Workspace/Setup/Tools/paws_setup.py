"""PAWS setup helper.

Standard library only. Works on Python 3.8 and later, with or without zoneinfo.
Run it from anywhere inside the workspace:

    python3 Setup/Tools/paws_setup.py status
    python3 Setup/Tools/paws_setup.py missing
    python3 Setup/Tools/paws_setup.py set owner.display_name "Colin"
    python3 Setup/Tools/paws_setup.py skip reader
    python3 Setup/Tools/paws_setup.py check-name "Garden Shed"
    python3 Setup/Tools/paws_setup.py preview
    python3 Setup/Tools/paws_setup.py apply --approved
    python3 Setup/Tools/paws_setup.py verify
    python3 Setup/Tools/paws_setup.py finish
    python3 Setup/Tools/paws_setup.py resume
    python3 Setup/Tools/paws_setup.py rename-unit unit-1 "Garden Shed" [--approved]

Setup State is the record. This helper reads it, changes only rows the owner
answered, writes the full plan to Setup Plan.md, saves a prior copy of every
file it changes in Setup/Recovery, and logs each step in the Setup Log.
"""
import argparse
import datetime
import hashlib
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.parse
from pathlib import Path

STAGES = ['default', 'selected', 'approved', 'applied', 'verified']
ID_RE = re.compile(r'^(executive|hub|example|unit-[1-9][0-9]?)$')
LINK_RE = re.compile(r'(?<!!)\[([^\]\n]*)\]\(([^)\n]+)\)')
RESERVED = {'setup', 'package', 'readme.md', 'agents.md', 'claude.md', 'terms.md', 'license.md', 'notice.md',
            'workspace settings.md', 'projects base.md', 'next actions.md', 'daily note.md',
            "needs the owner's decision.md", 'con', 'prn', 'aux', 'nul'}
QUESTIONS = {
    'owner.display_name': 'What should your assistants call you?',
    'hosts': 'Which AI app or command-line tool will you use with this folder?',
    'reader': 'What will you read the files in?',
    'calendar': 'Would you like to hear about using an outside calendar later? The Markdown calendar stays the record.',
    'writing_samples': 'Would you like to share some writing so the assistants can write like you?',
    'work_preferences': 'In a few sentences, how do you like to work?',
    'personas.review': 'Would you like to change any persona names or manner?',
    'boundaries': 'Is there anything your assistants can always send or update without asking? Anything off limits, or that you always want asked about first? Any quiet hours? Say skip to keep the page as it is.',
    'work_folders': 'Should I stay inside this workspace folder, or are there other folders I can use? Say skip to keep it to this folder.',
}
FOLDERS_Q = 'Should I stay inside this workspace folder, or are there other folders I can use?'
FOLDERS_DEFAULT = 'this workspace folder only.'
FOLDERS_SAME = re.compile(r'^(skip|none|no|nothing|default|(this |the )?workspace( folder)?( only)?|only (this |the )?workspace( folder)?|this folder( only)?|stay (inside|in) (this|the) (workspace )?folder)[.!]*$', re.I)


def folders_line(value):
    v = (value or '').strip()
    if not v or FOLDERS_SAME.match(v) or v.lower().rstrip('.') == FOLDERS_DEFAULT.rstrip('.'):
        return FOLDERS_DEFAULT
    v = v.rstrip('.')
    return 'this workspace folder, plus ' + v + '.'


# ---------- finding things ----------

def find_root(start=None):
    p = Path(start or Path(__file__).parent).resolve()
    for cand in [p] + list(p.parents):
        if (cand / 'Workspace Settings.md').is_file():
            return cand
    sys.exit('No Workspace Settings.md found. Run this inside a PAWS folder.')


def read(p):
    return p.read_text(encoding='utf-8')


def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]


def now_text():
    t = datetime.datetime.now().astimezone()
    return t.strftime('%Y-%m-%d %H:%M ') + (t.tzname() or t.strftime('%z'))


def setup_dir(root):
    m = re.search(r'^Current setup folder: `([^`]+)`$', read(root / 'Workspace Settings.md'), re.M)
    return root / (m.group(1) if m else 'Setup')


def split_row(line):
    cells, cur, i = [], '', 0
    body = line.strip()
    if body.startswith('|'):
        body = body[1:]
    if body.endswith('|') and not body.endswith('\\|'):
        body = body[:-1]
    while i < len(body):
        if body[i] == '\\' and i + 1 < len(body) and body[i + 1] == '|':
            cur += '|'
            i += 2
            continue
        if body[i] == '|':
            cells.append(cur.strip())
            cur = ''
        else:
            cur += body[i]
        i += 1
    cells.append(cur.strip())
    return cells


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def units(root):
    out = {}
    for line in read(root / 'Workspace Settings.md').splitlines():
        if line.startswith('|'):
            c = split_row(line)
            if len(c) >= 6 and ID_RE.match(c[0]) and c[0] not in out:
                links = [re.search(r'\]\(([^)]+)\)', x) for x in c[3:6]]
                paths = [(root / urllib.parse.unquote(m.group(1))).resolve() if m else None for m in links]
                # Columns: Profile | Desk | Unit page. The profile holds the job too.
                out[c[0]] = {'display': c[1], 'folder': c[2].strip('`'), 'persona': paths[0], 'role': paths[0], 'office': paths[1]}
    return out


# ---------- Setup State ----------

class State:
    def __init__(self, root):
        self.root = root
        self.path = setup_dir(root) / 'Setup State.md'
        self.lines = read(self.path).splitlines()
        self.head = next(i for i, l in enumerate(self.lines) if l.startswith('| Field |'))
        self.rows = []
        i = self.head + 2
        while i < len(self.lines) and self.lines[i].startswith('|'):
            c = split_row(self.lines[i])
            while len(c) < 5:
                c.append('')
            self.rows.append({'field': c[0], 'value': re.sub(r'\s*<!--.*?-->', '', c[1]).strip(), 'source': c[2], 'stage': c[3], 'ask': c[4]})
            i += 1
        self.end = i

    def line(self, key):
        for l in self.lines:
            if l.startswith(key + ': '):
                return l[len(key) + 2:]
        return ''

    def set_line(self, key, value):
        for i, l in enumerate(self.lines):
            if l.startswith(key + ': '):
                self.lines[i] = key + ': ' + value
                return
        self.lines.insert(2, key + ': ' + value)
        self.head += 1
        self.end += 1

    def row(self, field):
        for r in self.rows:
            if r['field'] == field:
                return r
        return None

    def open_choices(self):
        return [r for r in self.rows if r['ask'] == 'choice']

    def open_extras(self):
        return [r for r in self.rows if r['ask'] == 'extra']

    def next_question(self):
        if self.line('Status') == 'complete':
            return 'None. Setup is complete. A skipped extra can be picked up any time.'
        c = self.open_choices()
        if c:
            return question(c[0]['field'], self)
        if self.open_extras():
            return 'None. Show the short finish.'
        if any(r['stage'] == 'selected' for r in self.rows):
            return 'None. Show the short finish.'
        return 'None.'

    def progress(self):
        c, e = len(self.open_choices()), len(self.open_extras())
        words = ['No', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        n = words[c] if c < len(words) else str(c)
        first = n + (' choice left.' if c == 1 else ' choices left.')
        return first + ' Everything else keeps its default unless the owner raises it.'

    def save(self):
        self.set_line('Next question', self.next_question())
        self.set_line('Progress', self.progress())
        body = ['| ' + ' | '.join(cell(r[k]) for k in ('field', 'value', 'source', 'stage', 'ask')) + ' |' for r in self.rows]
        out = self.lines[:self.head + 2] + body + self.lines[self.end:]
        write(self.path, '\n'.join(out) + '\n')
        self.__init__(self.root)


def question(field, state=None):
    if field == 'boundaries' and state is not None:
        wf = state.row('work_folders')
        if wf and wf['ask'] == 'choice':
            return QUESTIONS['boundaries'].replace(' Say skip to keep the page as it is.', ' ' + FOLDERS_Q + ' Say skip to keep the defaults.')
    if field in QUESTIONS:
        return QUESTIONS[field]
    m = re.match(r'^(example|unit-\d+)\.purpose$', field)
    if m:
        name = state.row(m.group(1) + '.name')['value'] if state and state.row(m.group(1) + '.name') else m.group(1)
        return 'What is ' + name + ' for?'
    return 'What should ' + field + ' be?'


# ---------- checks ----------

def check_name(root, name, uid=None):
    """Return a list of problems with a folder or display name. Empty means fine."""
    problems = []
    if not name or name != name.strip():
        problems.append('Use a name with no spaces at the start or end.')
    if len(name) > 60:
        problems.append('Keep it to 60 characters or fewer.')
    if any(unicodedata.category(ch).startswith('C') for ch in name):
        problems.append('Remove control characters.')
    if re.search(r'[\\/:*?"<>|]', name) or name in ('.', '..') or name.endswith('.'):
        problems.append('Remove / \\ : * ? " < > | and any trailing dot.')
    key = unicodedata.normalize('NFKC', name).casefold()
    if key in RESERVED:
        problems.append('That name is used by the workspace itself. Pick another.')
    for other, u in units(root).items():
        if other != uid and unicodedata.normalize('NFKC', u['folder']).casefold() == key:
            problems.append('Another unit (' + other + ') already uses that name.')
    if (root / name).exists() and not (uid and units(root).get(uid, {}).get('folder') == name):
        problems.append('A file or folder called ' + name + ' already exists here.')
    return problems


def check_zone(name):
    try:
        import zoneinfo  # Python 3.9 and later
        try:
            zoneinfo.ZoneInfo(name)
            return True, ''
        except Exception:
            return False, 'That time zone was not found.'
    except ImportError:
        pass
    for base in ('/usr/share/zoneinfo', '/usr/lib/zoneinfo', '/usr/share/lib/zoneinfo'):
        if Path(base).is_dir():
            return ((Path(base) / name).is_file(), '' if (Path(base) / name).is_file() else 'That time zone was not found.')
    if re.match(r'^(UTC|[A-Z][A-Za-z_]+(/[A-Z][A-Za-z0-9_+-]+)+)$', name):
        return True, 'Could not confirm the zone on this computer. Ask the owner to confirm it.'
    return False, 'That does not look like a time zone name such as Asia/Tokyo.'


# ---------- planned changes ----------

def field_line(path, label, value):
    """Replace the value of a '- Label: value' or 'Label: value' line."""
    text = read(path)
    pat = re.compile(r'^(' + re.escape(label) + r': ).*$', re.M | re.I)
    if not pat.search(text):
        return None
    return pat.sub(lambda m: m.group(1) + value, text, count=1)


def persona_paths(root, uid):
    u = units(root).get(uid)
    return u if u else None


def changes_for(root, state, r):
    """Return a list of (path, new_text, note) for one selected row. Nothing is written."""
    f, v = r['field'], r['value']
    settings = root / 'Workspace Settings.md'
    out = []
    us = units(root)
    owner_md = None

    def add(path, text, note):
        if path is not None and text is not None and path.is_file() and text != read(path):
            out.append((path, text, note))

    if f == 'owner.display_name':
        add(settings, field_line(settings, '- Owner display name', v), 'owner name')
        if owner_md:
            add(owner_md, field_line(owner_md, '- Your name', v), 'owner name')
    elif f == 'owner.form_of_address':
        add(settings, field_line(settings, '- Form of address', v), 'form of address')
        if owner_md:
            add(owner_md, field_line(owner_md, '- How you like to be addressed', v), 'form of address')
    elif f == 'timezone':
        add(settings, field_line(settings, '- Time zone', v), 'time zone')
        if owner_md:
            add(owner_md, field_line(owner_md, '- Time zone', v), 'time zone')
    elif f == 'hosts':
        add(settings, field_line(settings, '- Hosts', v), 'hosts')
    elif f == 'reader':
        add(settings, field_line(settings, '- Reader', v), 'reader')
    elif f == 'calendar':
        add(settings, field_line(settings, '- External calendar', v), 'calendar')
    elif f == 'boundaries':
        page = root / 'Boundaries.md'
        if page.is_file():
            old = read(page)
            text = re.sub(r'^- Always fine to send or update without asking: .*\n- Off limits, or always ask first: .*\n- Quiet hours: .*$', lambda mm: '- What I said at setup: ' + v, old, count=1, flags=re.M)
            if text != old:
                text = re.sub(r'^Last changed: .*$', lambda mm: 'Last changed: ' + now_text() + ', at setup.', text, count=1, flags=re.M)
            add(page, text, 'boundaries')
    elif f == 'work_folders':
        page = root / 'Boundaries.md'
        if page.is_file():
            old = read(page)
            line = '- Folders I can use: ' + folders_line(v)
            text = re.sub(r'^- Folders I can use: .*$', lambda mm: line, old, count=1, flags=re.M)
            if text != old:
                text = re.sub(r'^Last changed: .*$', lambda mm: 'Last changed: ' + now_text() + ', at setup.', text, count=1, flags=re.M)
            add(page, text, 'work folders')
    elif f == 'workspace.name':
        add(settings, field_line(settings, '- workspace display name', v), 'workspace name')
    elif f == 'work_preferences' and 'executive' in us:
        sheet = voice_folder(root) / 'Voice Sheet.md'
        if sheet.is_file():
            text = read(sheet)
            block = '## Working preferences\n\nNotes from the owner about how they like to work. They grant no permission.\n\n' + v + '\n'
            if '## Working preferences' in text:
                text = re.sub(r'## Working preferences\n[\s\S]*?(?=\n## |\Z)', block, text, count=1)
            else:
                text = text.rstrip('\n') + '\n\n' + block
            add(sheet, text, 'working preferences')
    else:
        m = re.match(r'^(executive|hub|example|unit-\d+)\.(purpose|persona|lead_name|style)$', f)
        if m and m.group(1) in us:
            uid, what = m.group(1), m.group(2)
            u = us[uid]
            if what == 'purpose':
                add(settings, field_line(settings, '- ' + u['folder'] + ' purpose', v), 'unit purpose')
                readme = root / u['folder'] / 'README.md'
                if readme.is_file():
                    rt = re.sub(r'^Purpose: .*$', lambda mm: 'Purpose: ' + v, read(readme), count=1, flags=re.M)
                    rt = rt.replace("The owner picks this unit's subject. Don't assume one. Write the agreed purpose here and in Workspace Settings.", 'The owner set this purpose during setup. Change it here and in Workspace Settings if it changes.')
                    add(readme, rt, 'unit purpose')
                if u['role'] and u['role'].is_file():
                    rt = re.sub(r'(## Mission\n\n)[^\n]*', lambda mm: mm.group(1) + v, read(u['role']), count=1)
                    add(u['role'], rt, 'unit purpose')
                if 'executive' in us:
                    areas = root / us['executive']['folder'] / '00 Start Here' / 'Section 1' / 'Areas and Contexts.md'
                    if areas.is_file():
                        at = re.sub(r'^(\| ' + re.escape(uid) + r' \| [^|]* \| )[^|]*( \|)', lambda mm: mm.group(1) + v + mm.group(2), read(areas), count=1, flags=re.M)
                        add(areas, at, 'unit purpose')
                top = root / 'README.md'
                if top.is_file() and uid not in ('executive', 'hub'):
                    tt = re.sub(r'^(- `' + re.escape(u['folder']) + r'/`: [^.]*\.).*$', lambda mm: (mm.group(1) if 'subject you choose' not in mm.group(1) else '- `' + u['folder'] + '/`: led by its ' + (u['display'] or 'unit lead') + '.') + ' ' + v, read(top), count=1, flags=re.M)
                    add(top, tt, 'unit purpose')
            elif what in ('persona', 'lead_name') and u['persona']:
                p = u['persona']
                text = read(p)
                text = re.sub(r'^# Persona: .*$', '# Persona: ' + v, text, count=1, flags=re.M)
                text = re.sub(r'^Display name: .*$', 'Display name: ' + v, text, count=1, flags=re.M)
                add(p, text, 'persona name')
                stext = read(settings)
                stext = re.sub(r'^(\| ' + re.escape(uid) + r' \| )[^|]*( \|)', lambda mm: mm.group(1) + v + mm.group(2), stext, count=1, flags=re.M)
                add(settings, stext, 'persona name')
                top = root / 'README.md'
                if top.is_file() and u['display']:
                    add(top, read(top).replace('with ' + u['display'] + ', the ', 'with ' + v + ', the ', 1), 'persona name')
                roster = root / us['executive']['folder'] / '00 Start Here' / 'Section 1' / 'Staff Directory.md'
                if roster.is_file():
                    rtext = re.sub(r'^(\| ' + re.escape(uid) + r' \| )[^|]*( \|)', lambda mm: mm.group(1) + v + mm.group(2), read(roster), count=1, flags=re.M)
                    add(roster, rtext, 'persona name')
            elif what == 'style' and u['persona']:
                p = u['persona']
                text = read(p)
                text = re.sub(r'(## How I sound\n\n)[^\n]*', lambda mm: mm.group(1) + v, text, count=1)
                add(p, text, 'persona manner')
    return out


def voice_folder(root):
    m = re.search(r'^Current Voice folder: `([^`]+)`$', read(root / 'Workspace Settings.md'), re.M)
    return root / (m.group(1).rstrip('/') if m else '')


# ---------- moves with link repair ----------

def quote(path):
    return urllib.parse.quote(path, safe='/-._~')


def move_with_links(root, src, dst, dry=False):
    """Move src to dst inside root and repair every relative Markdown link. Returns changed files."""
    src, dst = src.resolve(), dst.resolve()
    if dst.exists():
        raise ValueError('Destination already exists: ' + str(dst.relative_to(root)) + '. Nothing was moved.')
    md = [p for p in root.rglob('*.md') if '.obsidian' not in p.parts and 'Recovery' not in p.parts]

    def mapped(p):
        try:
            return dst / p.relative_to(src)
        except ValueError:
            return p
    plan = []
    for f in md:
        text = read(f)
        newf = mapped(f)

        def fix(m):
            url = m.group(2).strip()
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url):
                return m.group(0)
            path, hashmark, frag = url.partition('#')
            if not path:
                return m.group(0)
            target = (f.parent / urllib.parse.unquote(path)).resolve()
            nt = mapped(target)
            if nt == target and newf == f:
                return m.group(0)
            relp = os.path.relpath(str(nt), str(newf.parent)).replace(os.sep, '/')
            return '[' + m.group(1) + '](' + quote(relp) + hashmark + frag + ')'
        new = LINK_RE.sub(fix, text)
        old_rel = str(src.relative_to(root)).replace(os.sep, '/')
        new_rel = str(dst.relative_to(root)).replace(os.sep, '/')
        new = new.replace('`' + old_rel + '/`', '`' + new_rel + '/`').replace('`' + old_rel + '`', '`' + new_rel + '`')
        if new != text:
            plan.append((f, newf, new))
    if dry:
        return [str(f.relative_to(root)) for f, _, _ in plan]
    shutil.move(str(src), str(dst))
    for f, newf, new in plan:
        write(newf, new)
    return [str(newf.relative_to(root)) for _, newf, _ in plan]


def rename_voice(root, owner):
    current = voice_folder(root)
    target = current.parent / (owner + "'s Voice")
    if not current.is_dir() or current == target or check_name_simple(owner + "'s Voice"):
        return None
    if target.exists():
        print('A folder called ' + target.name + ' already exists, so the Voice folder kept its name.')
        return None
    move_with_links(root, current, target)
    settings = root / 'Workspace Settings.md'
    old_rel = str(current.relative_to(root)).replace(os.sep, '/')
    new_rel = str(target.relative_to(root)).replace(os.sep, '/')
    write(settings, read(settings).replace('Current Voice folder: `' + old_rel + '/`', 'Current Voice folder: `' + new_rel + '/`'))
    return new_rel


def rename_display(root, old, new):
    """Replace the shown unit name as a whole word in every page except history, recovery copies and the legal files."""
    pat = re.compile(r'(?<![\w%])' + re.escape(old) + r'(?![\w%]|\.md|%20)')
    count = 0
    for p in root.rglob('*.md'):
        parts = set(p.relative_to(root).parts)
        if parts & {'.obsidian', 'Recovery', '.git'} or p.name in ('LICENSE.md', 'NOTICE.md', 'Setup Log.md', 'Setup Plan.md'):
            continue
        text = read(p)
        new_text = re.sub(r'\]\([^)]*\)|' + pat.pattern, lambda m: m.group(0) if m.group(0).startswith('](') else new, text)
        if new_text != text:
            write(p, new_text)
            count += 1
    return count


def check_name_simple(name):
    return bool(re.search(r'[\\/:*?"<>|]', name)) or any(unicodedata.category(ch).startswith('C') for ch in name)


# ---------- log ----------

def log_step(root, step, path, change, prior, result):
    log = setup_dir(root) / 'Setup Log.md'
    text = read(log)
    row = '| ' + ' | '.join(cell(x) for x in (step, path, change, prior, result)) + ' |'
    marker = '| Step | File | Change | Prior copy | Result |'
    if marker in text:
        lines = text.splitlines()
        i = lines.index(marker) + 2
        while i < len(lines) and lines[i].startswith('|'):
            i += 1
        lines.insert(i, row)
        text = '\n'.join(lines) + '\n'
    else:
        text = text.rstrip('\n') + '\n\n## Steps applied\n\n' + marker + '\n| --- | --- | --- | --- | --- |\n' + row + '\n'
    write(log, text)


def log_entry(root, what, files='none'):
    log = setup_dir(root) / 'Setup Log.md'
    text = read(log)
    row = '| ' + ' | '.join(cell(x) for x in (now_text(), 'setup helper', what, files)) + ' |'
    marker = '| When | Who | What happened | Files |'
    lines = text.splitlines()
    if marker in lines:
        i = lines.index(marker) + 2
        while i < len(lines) and lines[i].startswith('|'):
            i += 1
        lines.insert(i, row)
    else:
        lines += ['', '## Entries', '', marker, '| --- | --- | --- | --- |', row]
    write(log, '\n'.join(lines) + '\n')


# ---------- commands ----------

def cmd_status(root, a):
    s = State(root)
    print('Status: ' + s.line('Status'))
    print('Run by: ' + s.line('Run by'))
    print('Persona review: ' + s.line('Persona review'))
    print('Next question: ' + s.next_question())
    print('Progress: ' + s.progress())
    for name in ('LICENSE.md', 'NOTICE.md'):
        if not (root / name).is_file():
            print('Missing at the workspace root: ' + name + '. Say so to the owner. Never write legal text.')
    return 0


def cmd_missing(root, a):
    s = State(root)
    for r in s.open_choices():
        print('choice  ' + r['field'] + ': ' + question(r['field'], s) + ' Default: ' + r['value'])
    for r in s.open_extras():
        print('extra   ' + r['field'] + ': ' + question(r['field'], s) + ' Default: ' + r['value'])
    if not s.open_choices() and not s.open_extras():
        print('Nothing left to ask.')
    return 0


def cmd_set(root, a):
    s = State(root)
    r = s.row(a.field)
    if r is None:
        sys.exit('No row called ' + a.field + ' in Setup State. Run "missing" to see the fields.')
    value = a.value.strip()
    if a.field == 'timezone':
        ok, msg = check_zone(value)
        if not ok:
            sys.exit(msg)
        if msg:
            print(msg)
    if a.field.endswith('.name') and re.match(r'^(executive|hub|unit-\d+)\.name$', a.field):
        sys.exit('Unit folder names change through rename-unit, so the links get repaired.')
    if re.search(r'[\[\]`<>]|\]\(', value):
        sys.exit('Please use plain words, not links or markup.')
    r['value'], r['source'], r['stage'] = value, 'owner', 'selected'
    if r['ask'] in ('choice', 'extra'):
        r['ask'] = 'done'
    if a.field == 'personas.review':
        s.set_line('Persona review', 'done')
    s.save()
    print('Saved ' + a.field + '. ' + s.progress())
    return 0


def cmd_skip(root, a):
    s = State(root)
    r = s.row(a.field)
    if r is None:
        sys.exit('No row called ' + a.field + '.')
    if r['ask'] in ('choice', 'extra'):
        r['ask'] = 'skipped'
    wf = s.row('work_folders')
    if a.field == 'boundaries' and wf and wf['ask'] == 'choice':
        wf['ask'] = 'skipped'
    s.save()
    print('Skipped ' + a.field + '. The default stays: ' + r['value'] + '. ' + s.progress())
    return 0


def cmd_check_name(root, a):
    problems = check_name(root, a.name, a.unit)
    print('\n'.join(problems) if problems else 'That name is fine.')
    return 1 if problems else 0


def planned(root, s):
    out = []
    for r in s.rows:
        if r['stage'] in ('selected', 'approved'):
            out.append((r, changes_for(root, s, r)))
    return out


def cmd_preview(root, a):
    s = State(root)
    plan = planned(root, s)
    lines = ['# Setup Plan', '', 'Written ' + now_text() + '. Nothing here is saved until the owner approves it. The short version goes in chat. This page has the full detail.', '']
    lines += ['## Answers', '', '| Field | New value | Source |', '| --- | --- | --- |']
    for r, _ in plan:
        lines.append('| ' + cell(r['field']) + ' | ' + cell(r['value']) + ' | ' + cell(r['source']) + ' |')
    lines += ['', '## File changes', '']
    count = 0
    for r, changes in plan:
        for path, new, note in changes:
            count += 1
            old = read(path).splitlines()
            nl = new.splitlines()
            diff = [('- ' + x) for x in old if x not in nl][:12] + [('+ ' + x) for x in nl if x not in old][:12]
            lines += ['### ' + str(path.relative_to(root)).replace(os.sep, '/'), '', 'For ' + r['field'] + ' (' + note + ').', '', '```', *diff, '```', '']
    if not count:
        lines.append('No file changes. The answers only update Setup State.')
    lines += ['', '## How to undo', '', 'Before each change the helper copies the file into `Setup/Recovery/`. To undo, copy that file back over the changed one. The Setup Log lists every step.', '']
    write(setup_dir(root) / 'Setup Plan.md', '\n'.join(lines))
    s.set_line('Plan', 'shown ' + now_text() + ', see Setup Plan.md')
    s.save()
    files = sorted({str(p.relative_to(root)) for _, ch in plan for p, _, _ in ch})
    print('Answers to save: ' + str(len(plan)) + '. Files that change: ' + str(len(files)) + '.')
    for f in files[:8]:
        print('  ' + f)
    print('Full detail: ' + str((setup_dir(root) / 'Setup Plan.md').relative_to(root)))
    return 0


def cmd_apply(root, a):
    if not a.approved:
        sys.exit('Show the plan first. Run apply --approved once the owner says to finish.')
    s = State(root)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    recovery = setup_dir(root) / 'Recovery' / stamp
    saved = set()
    for r in s.rows:
        if r['stage'] == 'selected':
            r['stage'] = 'approved'
    s.save()
    for field in [r['field'] for r in State(root).rows if r['stage'] == 'approved']:
        fresh = State(root)
        r = fresh.row(field)
        changes = changes_for(root, fresh, r)
        for path, new, note in changes:
            relp = str(path.relative_to(root)).replace(os.sep, '/')
            if relp not in saved:
                write(recovery / relp, read(path))
                saved.add(relp)
            step = r['field'] + ':' + digest(new)
            log_step(root, step, relp, note + ' set to ' + r['value'], str((recovery / relp).relative_to(root)), 'started')
            write(path, new)
            log_step(root, step, relp, note, '', 'saved')
        m = re.match(r'^(executive|hub|example|unit-\d+)\.(persona|lead_name)$', field)
        if m and changes:
            u = units(root).get(m.group(1))
            if u and u['persona'] and u['persona'].is_file() and u['persona'].stem != r['value'] and not check_name_simple(r['value']):
                target = u['persona'].with_name(r['value'] + '.md')
                if not target.exists():
                    move_with_links(root, u['persona'], target)
                    log_step(root, field + ':file', str(target.relative_to(root)).replace(os.sep, '/'), 'Persona file renamed to match the name', '', 'saved')
    owner = State(root).row('owner.display_name')
    if owner and owner['stage'] == 'approved' and owner['value'] not in ('', '[Owner]'):
        moved = rename_voice(root, owner['value'])
        if moved:
            log_step(root, 'voice-folder', moved, 'Voice folder renamed for the owner name', '', 'saved')
    s = State(root)
    for r in s.rows:
        if r['stage'] == 'approved':
            r['stage'] = 'applied'
    s.set_line('Status', 'in progress')
    s.save()
    log_entry(root, 'Applied the approved plan.', str(len(saved)) + ' files')
    print('Applied. Changed ' + str(len(saved)) + ' files. Prior copies are in ' + str(recovery.relative_to(root)) + '. Run verify next.')
    return 0


def cmd_verify(root, a):
    s = State(root)
    bad = []
    for r in s.rows:
        if r['stage'] == 'applied':
            left = changes_for(root, s, r)
            if left:
                bad.append(r['field'] + ' is not in ' + ', '.join(str(p.relative_to(root)) for p, _, _ in left))
            else:
                r['stage'] = 'verified'
    s.save()
    checker = Path(__file__).with_name('check_package.py')
    code = subprocess.call([sys.executable, str(checker), str(root), '--mode', 'workspace'])
    for b in bad:
        print('Not saved yet: ' + b + '. Run resume, or apply --approved again.')
    if not bad and code == 0:
        print('Verified. Run finish to mark setup complete.')
    return 1 if bad or code else 0


def cmd_finish(root, a):
    s = State(root)
    waiting = [r['field'] for r in s.rows if r['stage'] in ('selected', 'approved', 'applied')]
    if waiting:
        sys.exit('Still waiting: ' + ', '.join(waiting) + '. Apply and verify first.')
    s.set_line('Status', 'complete')
    s.set_line('Completed', now_text())
    s.save()
    settings = root / 'Workspace Settings.md'
    text = re.sub(r'^Configuration state: .*$', 'Configuration state: complete', read(settings), count=1, flags=re.M)
    write(settings, text)
    log_entry(root, 'Setup complete. The session carries on into normal work.', 'Setup State.md, Workspace Settings.md')
    print('Setup is complete. Keep working in the same session. Change the Current Work cell of your Session Log row from setup to the next job, then offer the optional tour.')
    return 0


def cmd_resume(root, a):
    s = State(root)
    print('Status: ' + s.line('Status'))
    pending = [r for r in s.rows if r['stage'] in ('approved', 'applied')]
    redo = 0
    for r in pending:
        for path, new, note in changes_for(root, s, r):
            relp = str(path.relative_to(root)).replace(os.sep, '/')
            write(path, new)
            log_step(root, r['field'] + ':' + digest(new), relp, note + ' finished on resume', '', 'saved')
            redo += 1
        r['stage'] = 'applied'
    s.save()
    print('Finished ' + str(redo) + ' leftover changes. Next question: ' + State(root).next_question())
    return 0


def cmd_rename_unit(root, a):
    us = units(root)
    if a.unit not in us:
        sys.exit('No unit with stable ID ' + a.unit + '.')
    problems = check_name(root, a.name, a.unit)
    if problems:
        sys.exit('\n'.join(problems))
    old = us[a.unit]['folder']
    src, dst = root / old, root / a.name
    files = move_with_links(root, src, dst, dry=True)
    if not a.approved:
        print('Rename ' + old + ' to ' + a.name + '. Links to repair in ' + str(len(files)) + ' files. Run again with --approved once the owner agrees.')
        return 0
    changed = move_with_links(root, src, dst)
    settings = root / 'Workspace Settings.md'
    text = re.sub(r'^(\| ' + re.escape(a.unit) + r' \| [^|]* \| )' + re.escape(old) + r'( \|)', lambda m: m.group(1) + a.name + m.group(2), read(settings), count=1, flags=re.M)
    write(settings, text)
    shown = rename_display(root, old, a.name)
    st = State(root)
    row = st.row(a.unit + '.name')
    if row:
        row['value'], row['source'], row['stage'] = a.name, 'owner', 'applied'
        st.save()
    log_entry(root, 'Renamed unit ' + a.unit + ' from ' + old + ' to ' + a.name + ' and repaired links.', str(len(changed)) + ' files')
    print('Renamed. Repaired links in ' + str(len(changed)) + ' files and updated the shown name in ' + str(shown) + ' files. Run check_package.py --mode workspace to confirm.')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='PAWS setup helper')
    ap.add_argument('--root', help='workspace folder (default: found from this script)')
    sub = ap.add_subparsers(dest='cmd')
    sub.add_parser('status')
    sub.add_parser('missing')
    p = sub.add_parser('set')
    p.add_argument('field')
    p.add_argument('value')
    p = sub.add_parser('skip')
    p.add_argument('field')
    p = sub.add_parser('check-name')
    p.add_argument('name')
    p.add_argument('--unit')
    sub.add_parser('preview')
    p = sub.add_parser('apply')
    p.add_argument('--approved', action='store_true')
    sub.add_parser('verify')
    sub.add_parser('finish')
    sub.add_parser('resume')
    p = sub.add_parser('rename-unit')
    p.add_argument('unit')
    p.add_argument('name')
    p.add_argument('--approved', action='store_true')
    a = ap.parse_args(argv)
    root = find_root(a.root)
    fn = {'status': cmd_status, 'missing': cmd_missing, 'set': cmd_set, 'skip': cmd_skip, 'check-name': cmd_check_name,
          'preview': cmd_preview, 'apply': cmd_apply, 'verify': cmd_verify, 'finish': cmd_finish, 'resume': cmd_resume,
          'rename-unit': cmd_rename_unit}.get(a.cmd or 'status')
    return fn(root, a)


if __name__ == '__main__':
    sys.exit(main())
