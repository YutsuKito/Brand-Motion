#!/usr/bin/env python3
"""Diagnóstico não invasivo do ambiente de produção."""
from pathlib import Path
import shutil, subprocess, sys, importlib.util, json

print('BRAND MOTION V27 — Diagnóstico do ambiente')
print('Python:', sys.version.split()[0], sys.executable)
if sys.version_info < (3,10): print('ERRO: instale Python >= 3.10')
for package in ('playwright','numpy','PIL'):
    print(f'{package}:', 'OK' if importlib.util.find_spec(package) else 'FALTA (pip install -r requirements.txt)')
for command in ('ffmpeg', 'ffprobe'):
    executable=shutil.which(command)
    print(f'{command}:', executable or 'FALTA (https://ffmpeg.org/download.html)')
if importlib.util.find_spec('playwright'):
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            exe = Path(p.chromium.executable_path)
            print('Chromium Playwright:',exe if exe.exists() else 'Não instalado; navegador do sistema: '+str(next((shutil.which(n) for n in ('chromium','chromium-browser','google-chrome','google-chrome-stable') if shutil.which(n)),'não encontrado')))
    except Exception as e:
        print('Chromium Playwright: erro ao localizar:',str(e)[:260])
