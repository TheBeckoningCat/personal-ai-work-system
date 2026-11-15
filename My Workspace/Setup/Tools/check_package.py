"""Check a PAWS workspace or a PAWS download.

Standard library only. Works on Python 3.8 and later.

    python3 Setup/Tools/check_package.py --mode workspace
    python3 Setup/Tools/check_package.py --mode release path/to/download

release   checks a fresh download: manifest hashes, no live records, no app metadata.
workspace checks a folder in use: links, routes, unit rooms and setup records.
          Configured unit names, .obsidian files and live records are fine here.
Each problem comes with a suggested fix. Exit code 1 means at least one error.
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path

ID_RE = re.compile(r'^(executive|hub|example|unit-[1-9][0-9]?)$')
ROOMS_REQUIRED = ['01 Inbox', '40 Potential Projects']
ROOMS_STANDARD = ['10 Projects', '30 Calendar', '50 Offices', '80 SOPs']
DESK_PAGE = 'Desk.md'
META = {'.git', '.obsidian', '.DS_Store', '__pycache__', '.trash'}
STAGES = {'default', 'selected', 'approved', 'applied', 'verified'}
LINK_RE = re.compile(r'(?<!!)\[([^\]\n]*)\]\(([^)\n]+)\)')
SKIP_DIRS = {'.git', '.obsidian', '__pycache__', '.trash'}


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.notes = []
        self.counts = {}

    def error(self, where, problem, fix):
        self.errors.append({'where': where, 'problem': problem, 'fix': fix})

    def warn(self, where, problem, fix):
        self.warnings.append({'where': where, 'problem': problem, 'fix': fix})


def find_root(start):
    p = Path(start).resolve()
    for cand in [p] + list(p.parents):
        if (cand / 'Workspace Settings.md').is_file():
            return cand
    return None


def rel(root, p):
    return p.relative_to(root).as_posix()


def md_files(root):
    out = []
    for p in sorted(root.rglob('*.md')):
        parts = set(p.relative_to(root).parts)
        if parts & SKIP_DIRS:
            continue
        if 'Recovery' in parts or p.name == 'Setup Plan.md':
            continue
        out.append(p)
    return out


def slug(text):
    text = re.sub(r'<!--.*?-->', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    return re.sub(r'[^\w\- ]', '', text.lower(), flags=re.UNICODE).replace(' ', '-')


def headings(path):
    return [slug(m.group(1)) for m in re.finditer(r'^#{1,6}\s+(.+?)\s*#*$', path.read_text(encoding='utf-8'), re.M)]


def split_row(line):
    cells, cur, i = [], '', 0
    body = line.strip()
    if body.startswith('|'):
        body = body[1:]
    if body.endswith('|') and not body.endswith('\\|'):
        body = body[:-1]
    while i < len(body):
        ch = body[i]
        if ch == '\\' and i + 1 < len(body) and body[i + 1] == '|':
            cur += '|'
            i += 2
            continue
        if ch == '|':
            cells.append(cur.strip())
            cur = ''
        else:
            cur += ch
        i += 1
    cells.append(cur.strip())
    return cells


def link_target(root, from_file, raw):
    url = raw.strip()
    if url.startswith('<') and url.endswith('>'):
        url = url[1:-1].strip()
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url):
        return None, None
    path, _, frag = url.partition('#')
    if not path:
        return from_file, urllib.parse.unquote(frag)
    decoded = urllib.parse.unquote(path)
    if decoded.startswith('/'):
        return 'escape', None
    target = (from_file.parent / decoded).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return 'escape', None
    return target, urllib.parse.unquote(frag) if frag else None


def check_links(root, rep):
    links = anchors = 0
    for f in md_files(root):
        text = re.sub(r'```[\s\S]*?```', '', f.read_text(encoding='utf-8'))
        for m in LINK_RE.finditer(text):
            target, frag = link_target(root, f, m.group(2))
            if target is None:
                continue
            links += 1
            where = rel(root, f)
            if target == 'escape':
                rep.error(where, 'link leaves the workspace: ' + m.group(2), 'Point the link at a file inside the workspace, or write the outside path as plain text.')
                continue
            if not target.exists():
                rep.error(where, 'broken link: ' + m.group(2), 'Find where the page moved and update the link. If a folder was renamed, rerun the rename with Setup/Tools/paws_setup.py so links are repaired.')
                continue
            if frag and target.is_file() and target.suffix == '.md':
                anchors += 1
                if frag not in headings(target):
                    rep.error(where, 'link points at a heading that is not there: #' + frag, 'Change the link to an existing heading in ' + rel(root, target) + ', or drop the # part.')
    rep.counts['links_checked'] = links
    rep.counts['heading_links_checked'] = anchors


def mapping(root, rep):
    path = root / 'Workspace Settings.md'
    out = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        cells = split_row(line)
        if len(cells) >= 6 and ID_RE.match(cells[0]) and '](' in line and cells[0] not in out:
            out[cells[0]] = {'display': cells[1], 'folder': cells[2].strip('`'), 'cells': cells}
    if 'executive' not in out or 'hub' not in out:
        rep.error('Workspace Settings.md', 'the stable mapping table is missing the executive or hub row', 'Restore the rows for stable IDs executive and hub in the Stable mapping table.')
    return out


def check_mapping(root, rep, units):
    settings = root / 'Workspace Settings.md'
    for uid, row in units.items():
        folder = root / row['folder']
        if not folder.is_dir():
            rep.error('Workspace Settings.md', 'unit ' + uid + ' points at a folder that is not there: ' + row['folder'], 'Rename the folder back, or change the Physical Unit cell to the folder that exists now.')
            continue
        for room in ROOMS_REQUIRED + (['00 Start Here'] if uid == 'executive' else []):
            if not (folder / room).is_dir():
                rep.error(row['folder'], 'missing room ' + room, 'Copy the room from another unit, including its README.')
        for room in ROOMS_STANDARD:
            if not (folder / room).is_dir():
                rep.warn(row['folder'], 'missing standard room ' + room, 'Copy the room from another unit if this unit should have it.')
        for col, label in ((3, 'Profile'), (4, 'Desk'), (5, 'Unit page')):
            m = re.search(r'\]\(([^)]+)\)', row['cells'][col] if col < len(row['cells']) else '')
            target = link_target(root, settings, m.group(1))[0] if m else None
            if not m or target in (None, 'escape') or not target.is_file():
                rep.error('Workspace Settings.md', uid + ' has no working ' + label + ' link', 'Point the ' + label + ' cell at the right file for ' + uid + '.')


def check_directory(root, rep, units):
    if 'executive' not in units:
        return
    roster = root / units['executive']['folder'] / '00 Start Here' / 'Section 1' / 'Staff Directory.md'
    if not roster.is_file():
        rep.error(rel(root, roster.parent), 'Staff Directory.md is missing', 'Restore the Staff Directory in the executive unit Section 1.')
        return
    for line in roster.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        cells = split_row(line)
        if not (len(cells) >= 8 and ID_RE.match(cells[0]) and '](' in line):
            continue
        profile = re.search(r'\]\(([^)]+)\)', cells[5])
        desk = re.search(r'\]\(([^)]+)\)', cells[6])
        where = rel(root, roster)
        if not profile or not desk:
            rep.error(where, cells[0] + ' row lacks a Profile or Desk link', 'Fill in the Profile and Desk cells for ' + cells[0] + '.')
            continue
        pr = link_target(root, roster, profile.group(1))[0]
        if pr in (None, 'escape') or not pr.is_file():
            rep.error(where, cells[0] + ' profile is missing', 'Point the Profile link at that persona profile.')
        o = link_target(root, roster, desk.group(1))[0]
        if o in (None, 'escape') or not o.is_file() or o.name != DESK_PAGE:
            rep.error(where, cells[0] + ' desk page is missing', 'Point the Desk link at that persona office Desk.md. Copy one from the Desk template if it is gone.')
        if not cells[7].strip().strip('`').endswith('Incoming/'):
            rep.error(where, cells[0] + ' row lacks an Incoming path', 'Put the Incoming folder path in the last cell, like `Section 2/Mail Boxes/Title/Incoming/`.')


def setup_folder(root):
    text = (root / 'Workspace Settings.md').read_text(encoding='utf-8')
    m = re.search(r'^Current setup folder: `([^`]+)`$', text, re.M)
    return root / (m.group(1) if m else 'Setup')


def check_setup_state(root, rep):
    folder = setup_folder(root)
    state = folder / 'Setup State.md'
    if not state.is_file():
        rep.error(rel(root, folder) if folder.exists() else 'Setup', 'Setup State.md is missing', 'Check the Current setup folder line in Workspace Settings, or bring Setup back with the Setup Archive guide.')
        return
    lines = state.read_text(encoding='utf-8').splitlines()
    where = rel(root, state)
    if not any(l.startswith('Status: ') for l in lines):
        rep.error(where, 'no Status line', 'Add a line such as "Status: not started" under the title.')
    head = next((i for i, l in enumerate(lines) if l.startswith('| Field |')), None)
    if head is None:
        rep.error(where, 'the choices table is missing', 'Restore the table that starts with "| Field | Value | Source | Stage | Ask |".')
        return
    if head + 1 >= len(lines) or not re.match(r'^\|\s*-', lines[head + 1]):
        rep.error(where, 'the choices table has no separator row', 'Put "| --- | --- | --- | --- | --- |" right under the header row.')
    i = head + 2
    rows = 0
    while i < len(lines) and lines[i].startswith('|'):
        cells = split_row(lines[i])
        rows += 1
        if len(cells) != 5:
            rep.error(where, 'row ' + str(rows) + ' has ' + str(len(cells)) + ' cells, not 5', 'Escape any | inside a value as \\| and keep five cells.')
        elif cells[3] not in STAGES:
            rep.error(where, cells[0] + ' has an unknown stage ' + cells[3], 'Use default, selected, approved, applied or verified.')
        i += 1
    if i < len(lines) and lines[i].strip() == '' and i + 1 < len(lines) and lines[i + 1].startswith('|'):
        rep.error(where, 'a blank line splits the choices table', 'Delete the blank line so every row sits under the header.')
    rep.counts['setup_rows'] = rows
    for name in ['SETUP.md', 'Setup Log.md']:
        if not (folder / name).is_file():
            rep.error(rel(root, folder), name + ' is missing', 'Restore ' + name + ' in the setup folder.')


def clock_rows(root, units):
    if 'executive' not in units:
        return []
    clock = root / units['executive']['folder'] / '00 Start Here' / 'Section 1' / 'Session Log.md'
    rows = []
    if clock.is_file():
        for line in clock.read_text(encoding='utf-8').splitlines():
            if line.startswith('|') and not line.startswith('| Session ID') and not re.match(r'^\|\s*-', line):
                cells = split_row(line)
                if len(cells) >= 4 and cells[0]:
                    rows.append(cells)
    return rows


def check_release(root, rep, units):
    manifest = root / 'Package' / 'Package Manifest.json'
    if not manifest.is_file():
        rep.error('Package', 'Package Manifest.json is missing', 'Rebuild the download, or run in --mode workspace for a folder in use.')
    else:
        data = json.loads(manifest.read_text(encoding='utf-8'))
        listed = data.get('files', {})
        found = {}
        for p in sorted(root.rglob('*')):
            if p.is_file() and rel(root, p) != 'Package/Package Manifest.json':
                found[rel(root, p)] = hashlib.sha256(p.read_bytes()).hexdigest()
        for name in sorted(set(listed) | set(found)):
            if name not in found:
                rep.error(name, 'listed in the manifest but missing', 'Rebuild the download so the file comes back.')
            elif name not in listed:
                rep.error(name, 'not listed in the manifest', 'Remove the extra file, or rebuild the download.')
            elif listed[name] != found[name]:
                rep.error(name, 'changed since the download was built', 'Rebuild the download. For a folder in use, run --mode workspace instead.')
        rep.counts['manifest_files'] = len(listed)
    for p in root.rglob('*'):
        if set(p.relative_to(root).parts) & META:
            rep.error(rel(root, p), 'app or system metadata in a download', 'Delete it before sharing the download.')
            break
    if clock_rows(root, units):
        rep.error('Session Log.md', 'a fresh download should have no session rows', 'Clear the rows before sharing the download.')
    for p in root.rglob('Work Log/*.md'):
        if p.name != 'README.md':
            rep.error(rel(root, p), 'a fresh download should have no Work Log entries', 'Delete the entry before sharing the download.')
    for f in md_files(root):
        if re.search(r'test candidate', f.read_text(encoding='utf-8'), re.I):
            rep.error(rel(root, f), 'old "test candidate" wording', 'Remove the sentence. This is a release.')


def check_workspace(root, rep, units):
    rows = clock_rows(root, units)
    seen = set()
    for cells in rows:
        if cells[0] in seen:
            rep.error('Session Log.md', 'session ID used twice: ' + cells[0], 'Give the later session a new ID. One row per session.')
        seen.add(cells[0])
    active = [c for c in rows if len(c) > 3 and c[3] == 'in']
    for c in active:
        claim = c[6] if len(c) > 6 and c[6] else 'no claimed work'
        rep.notes.append('open session ' + c[0] + ' (' + c[1] + '): ' + claim)


def check_boundaries(root, rep):
    page = root / 'Boundaries.md'
    if not page.is_file():
        return
    text = page.read_text(encoding='utf-8')
    if not re.search(r'^## Where I can work\s*$', text, re.M):
        rep.error('Boundaries.md', 'the Where I can work section is missing', 'Restore the Where I can work heading. It says the helpers work only inside this workspace folder and any folders listed there.')
    if not re.search(r'^- Folders I can use: \S', text, re.M):
        rep.error('Boundaries.md', 'the Folders I can use line is missing', 'Restore the line "- Folders I can use: this workspace folder only." or the folders the owner listed.')


def run(root, mode):
    rep = Report()
    for name in ['README.md', 'AGENTS.md', 'LICENSE.md', 'NOTICE.md', 'Workspace Settings.md', 'Boundaries.md', 'Daily Note.md', 'Terms.md']:
        if not (root / name).is_file():
            fix = 'Copy LICENSE.md and NOTICE.md from the original download. Never write new legal text.' if name in ('LICENSE.md', 'NOTICE.md') else 'Restore ' + name + ' at the workspace root.'
            rep.error(name, 'missing at the workspace root', fix)
    if not (root / 'Workspace Settings.md').is_file():
        return rep
    units = mapping(root, rep)
    rep.counts['units'] = len(units)
    check_mapping(root, rep, units)
    check_directory(root, rep, units)
    check_links(root, rep)
    check_setup_state(root, rep)
    check_boundaries(root, rep)
    if mode == 'release':
        check_release(root, rep, units)
    else:
        check_workspace(root, rep, units)
    rep.counts['markdown_files'] = len(md_files(root))
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description='Check a PAWS workspace or download.')
    ap.add_argument('root', nargs='?', help='workspace folder (default: found from this script)')
    ap.add_argument('--mode', choices=['release', 'workspace'], default='workspace')
    ap.add_argument('--json', action='store_true', help='print the report as JSON')
    a = ap.parse_args(argv)
    root = find_root(a.root or Path(__file__).parent)
    if root is None:
        print('No Workspace Settings.md found. Run this from inside a PAWS folder or pass the folder.')
        return 2
    rep = run(root, a.mode)
    if a.json:
        print(json.dumps({'mode': a.mode, 'root': str(root), 'counts': rep.counts, 'errors': rep.errors, 'warnings': rep.warnings, 'notes': rep.notes}, indent=2, ensure_ascii=False))
    else:
        print('PAWS check, ' + a.mode + ' mode: ' + str(root))
        print(', '.join(k.replace('_', ' ') + ' ' + str(v) for k, v in rep.counts.items()))
        for kind, items in (('Error', rep.errors), ('Warning', rep.warnings)):
            for e in items:
                print(kind + ' in ' + e['where'] + ': ' + e['problem'] + '\n  Fix: ' + e['fix'])
        for n in rep.notes:
            print('Note: ' + n)
        print(str(len(rep.errors)) + ' errors, ' + str(len(rep.warnings)) + ' warnings.')
    return 1 if rep.errors else 0


if __name__ == '__main__':
    sys.exit(main())
