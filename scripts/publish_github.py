"""Reviewable publication helper. Dry-run is default; publishing never closes issues."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', help='GitHub OWNER/REPOSITORY')
    parser.add_argument('--publish', action='store_true', help='Create a public repository, push commits and open real issues now')
    parser.add_argument('--dry-run', action='store_true', help='Print commands only (default)')
    args = parser.parse_args()
    if args.publish and args.dry_run:
        parser.error('Choose --publish or --dry-run, not both.')
    parts = args.repository.split('/')
    if len(parts) != 2 or not all(part and all(c.isalnum() or c in '-_.' for c in part) for part in parts):
        parser.error('Use a valid OWNER/REPOSITORY name.')
    specs = sorted((ROOT / '_docs/issues').glob('*.md'))
    if len(specs) != 6:
        raise SystemExit('Expected six issue specification files.')
    commands = [
        ['gh', 'repo', 'create', args.repository, '--public', '--source', '.', '--remote', 'origin', '--push'],
    ]
    for spec in specs:
        title = spec.read_text(encoding='utf-8').splitlines()[0].removeprefix('# ')
        commands.append(['gh','issue','create','--repo',args.repository,'--title',title,'--body-file',str(spec)])
    if not args.publish:
        print('DRY RUN: no repository, issues or files are changed.')
        for command in commands:
            print(json.dumps(command, ensure_ascii=False))
        return
    subprocess.run(['python','-m','pytest','-q'], cwd=ROOT, check=True)
    subprocess.run(['gh','auth','status'], cwd=ROOT, check=True)
    if subprocess.run(['git','diff','--quiet'], cwd=ROOT).returncode or subprocess.run(['git','diff','--cached','--quiet'], cwd=ROOT).returncode:
        raise SystemExit('Commit tracked changes before publishing.')
    if subprocess.run(['git','remote','get-url','origin'], cwd=ROOT, capture_output=True).returncode == 0:
        raise SystemExit('origin already exists. Review and publish manually to avoid changing an existing remote.')
    issue_urls = []
    subprocess.run(commands[0], cwd=ROOT, check=True)
    for command in commands[1:]:
        issue_urls.append(subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip())
    print('Published repository and opened issues at the current real time. No issue was closed.')
    for spec, url in zip(specs, issue_urls):
        print(f'{spec.name}: {url}')
    print('Record real URLs in the ledger. Review published commits and QA evidence before manually closing accepted issues.')

if __name__ == '__main__':
    main()
