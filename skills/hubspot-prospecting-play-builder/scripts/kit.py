#!/usr/bin/env python3
"""Portable structural validation and CSV export. Python 3 standard library only."""
import argparse
import csv
import datetime as dt
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

SKILL = Path(__file__).resolve().parents[1]
SCHEMAS = {
    'Selected Play': ['section', 'decision', 'recommendation', 'evidence_status', 'source_or_gap'],
    'Signal Catalog': ['signal_id', 'signal', 'category', 'object_level', 'meaning', 'prerequisites', 'use_cases', 'crm_reengagement', 'availability', 'source_url', 'checked_on'],
    'CRM Reengagement': ['mapping_id', 'trigger_type', 'trigger', 'required_data', 'associations', 'eligibility', 'timing', 'exclusions', 'owner', 'message_angle', 'enrollment_route', 'verification'],
    'Play Library': ['play_id', 'play', 'relationship', 'trigger', 'offer_angle', 'required_evidence', 'exclusions', 'cta', 'next_priority'],
    'Evidence & Gaps': ['item_id', 'type', 'claim_or_gap', 'source', 'checked_on', 'status', 'next_action'],
}
CONTEXT_FILES = ['01-what-we-sell.txt', '02-value-proposition.txt', '03-pain-points.txt']
OUTREACH_FILES = {'adaptive': '04-advanced-instructions.txt', 'sequence': '04-sequence-steps.txt'}
DECISIONS = ['offer', 'audience', 'persona', 'relationship', 'trigger', 'eligibility', 'exclusions', 'sender_owner', 'review_mode', 'outreach_method', 'cadence', 'send_window_timezone', 'cta_policy', 'stop_conditions', 'enrollment_route', 'deliverability', 'credit_budget']


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def counts(text):
    return {'characters': len(text), 'utf16_units': len(text.encode('utf-16-le')) // 2}


def csv_name(sheet):
    return re.sub(r'[^a-z0-9]+', '-', sheet.lower()).strip('-') + '.csv'


def cell_text(value):
    return '' if value is None else str(value)


def safe_cell(value):
    """Export untrusted text as literal content, not a spreadsheet formula."""
    text = cell_text(value)
    if isinstance(value, str) and text.lstrip().startswith(('=', '+', '-', '@')):
        return "'" + text
    return text


def date_ok(value):
    try:
        dt.date.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False


def check_catalog(catalog, errors):
    signals = catalog.get('signals', [])
    if not signals:
        errors.append('Catalog must contain signal rows.')
    ids = [row.get('signal_id') for row in signals]
    names = [row.get('signal') for row in signals]
    if len(set(ids)) != len(ids) or len(set(names)) != len(names):
        errors.append('Catalog contains duplicate signal IDs or names.')
    if catalog.get('catalog_count') != len(signals):
        errors.append('Catalog catalog_count does not match its rows.')
    public_count = sum(row.get('source_type') == 'public_documentation' for row in signals)
    if catalog.get('documented_count') != public_count:
        errors.append('Catalog documented_count does not match public-documentation rows.')
    if not date_ok(catalog.get('checked_on')):
        errors.append('Catalog checked_on must be an ISO date.')
    for row in signals:
        for key in SCHEMAS['Signal Catalog']:
            if not cell_text(row.get(key)).strip():
                errors.append('Catalog row %s is missing %s.' % (row.get('signal_id'), key))
        if row.get('object_level') not in ('Company', 'Contact'):
            errors.append('Catalog row has unsupported object level: %s' % row.get('signal_id'))
        if row.get('source_type') not in ('public_documentation', 'account_observation'):
            errors.append('Catalog row needs public_documentation or account_observation source_type.')
        if not date_ok(row.get('checked_on')):
            errors.append('Catalog row has invalid checked_on: %s' % row.get('signal_id'))
    return signals


def check_tables(tables, errors):
    if set(tables) != set(SCHEMAS):
        errors.append('tables.json must contain exactly the five documented tables.')
    for sheet, columns in SCHEMAS.items():
        rows = tables.get(sheet, [])
        if not isinstance(rows, list) or not rows:
            errors.append('Table is empty or not a list: %s' % sheet)
            continue
        for number, row in enumerate(rows, 1):
            if not isinstance(row, dict) or set(row) != set(columns):
                errors.append('%s row %s has incorrect columns.' % (sheet, number))
                continue
            if any(isinstance(value, (list, dict)) for value in row.values()):
                errors.append('%s row %s has nested cell data; use scalar values.' % (sheet, number))
    decisions = {row.get('decision') for row in tables.get('Selected Play', [])}
    if not set(DECISIONS).issubset(decisions):
        errors.append('Selected Play is missing decisions: ' + ', '.join(sorted(set(DECISIONS) - decisions)))
    plays = tables.get('Play Library', [])
    if len(plays) < 10 or len({row.get('play_id') for row in plays}) != len(plays):
        errors.append('Play Library must contain at least ten distinct examples.')
    for sheet, key in [('Signal Catalog', 'signal_id'), ('CRM Reengagement', 'mapping_id'), ('Evidence & Gaps', 'item_id')]:
        ids = [row.get(key) for row in tables.get(sheet, [])]
        if any(not value for value in ids) or len(set(ids)) != len(ids):
            errors.append('%s contains empty or duplicate IDs.' % sheet)


def export_csv(run):
    tables = read_json(run / 'tables.json')
    errors = []
    check_tables(tables, errors)
    if errors:
        return {'ok': False, 'errors': errors}
    out = run / 'csv'
    out.mkdir(parents=True, exist_ok=True)
    for sheet, columns in SCHEMAS.items():
        with (out / csv_name(sheet)).open('w', encoding='utf-8-sig', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(columns)
            for row in tables[sheet]:
                writer.writerow([safe_cell(row[key]) for key in columns])
    return {'ok': True, 'files': [str(out / csv_name(sheet)) for sheet in SCHEMAS], 'note': 'Potential formula text is escaped with an apostrophe.'}


def workbook_rows(path):
    """Read saved table values for fidelity checks; no Excel dependency."""
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    rel_ns = '{http://schemas.openxmlformats.org/package/2006/relationships}'
    doc_rel = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
    with zipfile.ZipFile(path) as book:
        strings = []
        if 'xl/sharedStrings.xml' in book.namelist():
            for item in ET.fromstring(book.read('xl/sharedStrings.xml')).findall('m:si', ns):
                strings.append(''.join(t.text or '' for t in item.findall('.//m:t', ns)))
        style_dates = set()
        if 'xl/styles.xml' in book.namelist():
            styles = ET.fromstring(book.read('xl/styles.xml'))
            custom = {int(x.attrib['numFmtId']): x.attrib['formatCode'] for x in styles.findall('m:numFmts/m:numFmt', ns)}
            for i, style in enumerate(styles.findall('m:cellXfs/m:xf', ns)):
                fmt = int(style.attrib.get('numFmtId', 0))
                code = re.sub(r'"[^"]*"', '', custom.get(fmt, '')).lower()
                if fmt in range(14, 23) or ('y' in code and 'd' in code):
                    style_dates.add(i)
        wb = ET.fromstring(book.read('xl/workbook.xml'))
        props = wb.find('m:workbookPr', ns)
        base = dt.datetime(1904, 1, 1) if props is not None and props.attrib.get('date1904') in ('1', 'true') else dt.datetime(1899, 12, 30)
        rels = {item.attrib['Id']: item.attrib['Target'] for item in ET.fromstring(book.read('xl/_rels/workbook.xml.rels')).findall(rel_ns + 'Relationship')}
        result = {}
        for sheet in wb.findall('m:sheets/m:sheet', ns):
            target = rels[sheet.attrib[doc_rel]]
            xml_path = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            cells = {}
            for cell in ET.fromstring(book.read(xml_path)).findall('.//m:sheetData/m:row/m:c', ns):
                if cell.find('m:f', ns) is not None:
                    raise ValueError('Unexpected formula in text-only preparation workbook: ' + cell.attrib['r'])
                raw = cell.find('m:v', ns)
                value = raw.text if raw is not None else ''
                if cell.attrib.get('t') == 's':
                    value = strings[int(value)]
                elif cell.attrib.get('t') == 'inlineStr':
                    value = ''.join(t.text or '' for t in cell.findall('.//m:t', ns))
                elif value and int(cell.attrib.get('s', 0)) in style_dates:
                    value = (base + dt.timedelta(days=float(value))).date().isoformat()
                match = re.fullmatch(r'([A-Z]+)(\d+)', cell.attrib['r'])
                col = 0
                for char in match.group(1):
                    col = col * 26 + ord(char) - 64
                cells[(int(match.group(2)), col)] = value or ''
            result[sheet.attrib['name']] = cells
        return result


def validate_package():
    errors, warnings = [], []
    entry = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    if not entry.startswith('---\n') or 'name: hubspot-prospecting-play-builder' not in entry:
        errors.append('Skill frontmatter/name missing.')
    for path in SKILL.rglob('*'):
        if path.is_symlink():
            errors.append('Symlink is not portable: ' + str(path.relative_to(SKILL)))
        if not path.is_file() or path.suffix not in ('.md', '.txt', '.json', '.yaml', '.py'):
            continue
        text = path.read_text(encoding='utf-8')
        if re.search(r'[/]Users[/]|[/]home[/][^/]+[/]|[A-Z]:\\Users\\', text):
            errors.append('Machine-specific path: ' + str(path.relative_to(SKILL)))
        if path.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', text):
                link = link.strip('<>').split('#')[0]
                if not link or urlparse(link).scheme:
                    continue
                target = (path.parent / link).resolve()
                if SKILL not in target.parents or not target.exists():
                    errors.append('Missing/nonportable reference: %s -> %s' % (path.name, link))
    catalog = read_json(SKILL / 'assets/signal-catalog.json')
    signals = check_catalog(catalog, errors)
    recipes = read_json(SKILL / 'assets/crm-recipes.json')
    recipe_ids = {row['mapping_id'] for row in recipes}
    for row in signals:
        if row.get('recipe_id') not in recipe_ids:
            errors.append('Unknown recipe for ' + row['signal_id'])
    for row in recipes:
        if set(row) != set(SCHEMAS['CRM Reengagement']):
            errors.append('Recipe columns differ from delivery contract: ' + row.get('mapping_id', '?'))
    library = read_json(SKILL / 'assets/play-library.json')
    if len(library) < 10 or len({row['play_id'] for row in library}) != len(library):
        errors.append('Packaged Play library must contain at least ten unique examples.')
    base = (SKILL / 'assets/advanced-instructions-base.txt').read_text(encoding='utf-8')
    if max(counts(base).values()) >= 10000:
        errors.append('Instruction base is not below 10,000 characters.')
    return {'ok': not errors, 'errors': errors, 'warnings': warnings, 'catalog_count': len(signals), 'instruction_base': counts(base)}


def validate_run(run):
    errors, warnings = [], []
    if not (run / 'run.json').is_file():
        return {'ok': False, 'errors': ['Missing files: run.json']}
    manifest = read_json(run / 'run.json')
    method = manifest.get('outreach_method')
    if method not in OUTREACH_FILES:
        return {'ok': False, 'errors': ['outreach_method must be adaptive or sequence.']}
    copy_files = CONTEXT_FILES + [OUTREACH_FILES[method]]
    required = ['tables.json', 'catalog.json', 'setup-guide.md', 'illustrative-emails.md'] + copy_files
    missing = [name for name in required if not (run / name).is_file()]
    if missing:
        return {'ok': False, 'errors': ['Missing files: ' + ', '.join(missing)]}
    for key in ['company_url', 'prepared_on', 'selected_play_id', 'crm_mode', 'readiness', 'catalog_status', 'delivery_format', 'audience_confirmed', 'offer_confirmed']:
        if key not in manifest:
            errors.append('run.json missing ' + key)
    if manifest.get('crm_mode') not in ('none', 'export', 'connector'):
        errors.append('crm_mode must be none, export, or connector.')
    if manifest.get('readiness') not in ('draft', 'ready_for_preview'):
        errors.append('readiness must be draft or ready_for_preview.')
    if manifest.get('catalog_status') not in ('snapshot', 'refreshed'):
        errors.append('catalog_status must be snapshot or refreshed.')
    if manifest.get('delivery_format') not in ('csv', 'xlsx'):
        errors.append('delivery_format must be csv or xlsx.')
    if not date_ok(manifest.get('prepared_on')):
        errors.append('prepared_on must be an ISO date.')
    if urlparse(manifest.get('company_url', '')).scheme not in ('https', 'http'):
        errors.append('company_url must be an HTTP(S) URL.')
    ready = manifest.get('readiness') == 'ready_for_preview'
    if ready and not (manifest.get('audience_confirmed') is True and manifest.get('offer_confirmed') is True):
        errors.append('Ready for preview requires confirmed offer and audience.')
    file_counts = {}
    for name in copy_files:
        text = (run / name).read_text(encoding='utf-8')
        file_counts[name] = counts(text)
        if not text.strip():
            (errors if ready else warnings).append('No supported copy provided yet: ' + name)
        if re.search(r'\{\{[^}]+\}\}|\[(?:company|offer|name|resource)\]|\bTODO\b|\bTBD\b', text, re.I):
            errors.append('Unresolved placeholder in copy file: ' + name)
    if method == 'adaptive' and max(file_counts[OUTREACH_FILES['adaptive']].values()) >= 10000:
        errors.append('Advanced Instructions must be below 10,000 characters/UTF-16 units, including additions.')
    if not re.search(r'^#+\s*launch readiness', (run / 'setup-guide.md').read_text(encoding='utf-8'), re.I | re.M):
        (errors if ready else warnings).append('setup-guide.md has no Launch readiness section.')
    catalog = read_json(run / 'catalog.json')
    signals = check_catalog(catalog, errors)
    if manifest.get('catalog_status') == 'snapshot':
        warnings.append('Using dated snapshot; no live signal-catalog refresh claimed.')
    elif not manifest.get('catalog_refresh_source') or catalog.get('checked_on') != manifest.get('prepared_on'):
        errors.append('A refreshed catalog requires same-run date and catalog_refresh_source.')
    if date_ok(catalog.get('checked_on')) and date_ok(manifest.get('prepared_on')):
        age = (dt.date.fromisoformat(manifest['prepared_on']) - dt.date.fromisoformat(catalog['checked_on'])).days
        if age < 0:
            errors.append('Catalog check date is after preparation date.')
        elif age > 30:
            warnings.append('Signal snapshot is more than 30 days old; refresh or clearly flag staleness.')
    ui = catalog.get('reference_ui_observation', {})
    if ui.get('picker_count') != len(signals) and not ui.get('reconciled', False):
        warnings.append('Reference picker/catalog count discrepancy remains unresolved; do not claim full account coverage.')
    tables = read_json(run / 'tables.json')
    check_tables(tables, errors)
    if errors:
        return {'ok': False, 'errors': errors, 'warnings': warnings, 'copy_counts': file_counts}
    by_id = {row['signal_id']: row for row in signals}
    rendered = {row['signal_id']: row for row in tables['Signal Catalog']}
    if set(by_id) != set(rendered):
        errors.append('Signal Catalog must cover every row in the run catalog exactly once.')
    for key in set(by_id) & set(rendered):
        for field in ('signal', 'category', 'object_level', 'meaning', 'source_url', 'checked_on'):
            if by_id[key][field] != rendered[key][field]:
                errors.append('Signal source field differs from run catalog: %s/%s' % (key, field))
    if manifest.get('selected_play_id') not in {row['play_id'] for row in tables['Play Library']}:
        errors.append('Selected Play ID must be represented in Play Library.')
    if manifest.get('crm_mode') == 'none' and any(row['verification'].lower().startswith('verified') for row in tables['CRM Reengagement']):
        errors.append('URL-only runs cannot claim verified CRM mappings.')
    for name in ('setup-guide.md', 'illustrative-emails.md'):
        if not (run / name).read_text(encoding='utf-8').strip():
            errors.append('Required document is empty: ' + name)
    if manifest.get('delivery_format') == 'csv':
        for sheet, columns in SCHEMAS.items():
            path = run / 'csv' / csv_name(sheet)
            if not path.is_file():
                errors.append('Missing CSV: ' + path.name)
                continue
            with path.open(encoding='utf-8-sig', newline='') as handle:
                actual = list(csv.reader(handle))
            expected = [columns] + [[safe_cell(row[key]) for key in columns] for row in tables[sheet]]
            if actual != expected:
                errors.append('CSV differs from tables.json: ' + path.name)
    elif manifest.get('delivery_format') == 'xlsx':
        path = run / 'play-workbook.xlsx'
        if not path.is_file():
            errors.append('Missing play-workbook.xlsx.')
        else:
            actual = workbook_rows(path)
            if set(actual) != set(SCHEMAS):
                errors.append('Workbook must contain the five specified sheets.')
            for sheet, columns in SCHEMAS.items():
                expected = [columns] + [[cell_text(row[key]) for key in columns] for row in tables[sheet]]
                cells = actual.get(sheet, {})
                for ri, row in enumerate(expected, 1):
                    for ci, value in enumerate(row, 1):
                        # Writers may store safe formula-looking text with an apostrophe.
                        if cells.get((ri, ci), '') not in (value, safe_cell(value)):
                            errors.append('Workbook value differs: %s row %s column %s.' % (sheet, ri, ci))
                if any(value and (ri > len(expected) or ci > len(columns)) for (ri, ci), value in cells.items()):
                    errors.append('Unexpected populated cells beyond table: ' + sheet)
    return {'ok': not errors, 'errors': errors, 'warnings': warnings, 'readiness': manifest.get('readiness'), 'copy_counts': file_counts, 'signal_rows': len(signals), 'note': 'Structural checks only; truth, eligibility, copy quality, and visual layout require review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate-package', 'export-csv', 'validate-run'])
    parser.add_argument('run_dir', nargs='?', type=Path)
    args = parser.parse_args()
    if args.command != 'validate-package' and args.run_dir is None:
        parser.error('run_dir is required for this command')
    try:
        result = validate_package() if args.command == 'validate-package' else export_csv(args.run_dir) if args.command == 'export-csv' else validate_run(args.run_dir)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, zipfile.BadZipFile, ET.ParseError) as exc:
        result = {'ok': False, 'errors': [str(exc)]}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
