#!/usr/bin/env python3
"""Instala a skill via cópia no local esperado pelo agente (sem alterar outros arquivos)."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = ROOT.name
AGENTS = ('codex', 'claude', 'opencode', 'hermes')

def destination(agent: str, scope: str, project_root: Path) -> Path:
    home = Path.home()
    if agent == 'hermes':
        return home / '.hermes' / 'skills' / SKILL_NAME
    if scope == 'project':
        prefix = {'codex': '.agents', 'claude': '.claude', 'opencode': '.opencode'}[agent]
        return project_root / prefix / 'skills' / SKILL_NAME
    prefix = {
        'codex': home / '.agents',
        'claude': home / '.claude',
        'opencode': home / '.config' / 'opencode'
    }[agent]
    return prefix / 'skills' / SKILL_NAME


def skip_dir(path: Path):
    return path.name in {'frames', 'output', '__pycache__', '.venv', '.git', '.pytest_cache'}


def ignore(path, names):
    return [n for n in names if n in {'frames', 'output', '__pycache__', '.venv', '.git', '.pytest_cache'} or n.endswith(('.mp4', '.wav', '.pyc'))]


def main():
    parser = argparse.ArgumentParser(description='Instala Brand Motion V27 nos agentes compatíveis')
    parser.add_argument('--agent', choices=(*AGENTS, 'all'), default='all')
    parser.add_argument('--scope', choices=('user','project'), default='user')
    parser.add_argument('--root', type=Path, default=Path.cwd(), help='pasta do projeto')
    parser.add_argument('--replace', action='store_true', help='permite substituir instalação da skill')
    parser.add_argument('--dry-run', action='store_true', help='mostra destinos sem copiar')
    args = parser.parse_args()
    for agent in AGENTS if args.agent == 'all' else (args.agent,):
        dest = destination(agent, args.scope, args.root.resolve())
        print(f'{agent:9} -> {dest}')
        if args.dry_run: continue
        if dest.resolve() == ROOT.resolve():
            print('  [já é a pasta-fonte]'); continue
        if dest.exists():
            if not args.replace:
                print('  [pulado: destino já existe; use --replace para atualizar]')
                continue
            if not (dest / 'SKILL.md').is_file():
                raise SystemExit(f'Recusado substituir {dest}: não parece instalação de skill')
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(ROOT, dest, ignore=ignore)
        print('  [instalada]')

if __name__ == '__main__':
    main()
