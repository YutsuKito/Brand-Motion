#!/usr/bin/env python3
"""Valida projeto, assets e sincronização sem alterar arquivos."""
import argparse, json, sys
from pathlib import Path
KINDS={'software','product','store','service'}

def load(config: Path):
    config=config.resolve()
    obj=json.loads(config.read_text(encoding='utf-8'))
    errors=[]; warnings=[]
    v=obj.get('video',{}); brand=obj.get('brand',{})
    if not brand.get('name'): errors.append('brand.name obrigatório')
    if not obj.get('cta',{}).get('primary'): errors.append('cta.primary obrigatório')
    for k in ('width','height','fps'):
        if not isinstance(v.get(k),int) or v[k] <= 0: errors.append(f'video.{k} deve ser inteiro positivo')
    for k in ('explain_seconds','focus_seconds','transition_seconds','cta_seconds'):
        if not isinstance(v.get(k), (int,float)) or v[k] < .1: errors.append(f'video.{k} deve ser positivo')
    if (v.get('width',1920),v.get('height',1080)) != (1920,1080):
        warnings.append('A composição base usa 1920x1080; ajuste CSS/layout antes de mudar resolução')
    logo=brand.get('logo')
    if logo:
        p=(config.parent/logo).resolve()
        if not p.is_relative_to(config.parent) or not p.is_file(): errors.append('brand.logo não existe ou está fora do projeto')
    scenes=obj.get('scenes',[])
    if not isinstance(scenes,list) or not scenes: errors.append('Ao menos 1 cena é necessária')
    for i,s in enumerate(scenes):
        prefix=f'scenes[{i}]'
        if s.get('kind') not in KINDS: errors.append(f'{prefix}.kind inválido')
        for key in ('label','title','explanation','asset'):
            if not s.get(key): errors.append(f'{prefix}.{key} obrigatório')
        if len(s.get('title',''))>60: warnings.append(f'{prefix}.title extenso; simplifique')
        if len(s.get('explanation',''))>160: warnings.append(f'{prefix}.explanation extensa; reduza para ~80 caracteres')
        asset=s.get('asset')
        if asset:
            p=(config.parent/asset).resolve()
            if not p.is_relative_to(config.parent): errors.append(f'{prefix}.asset fora do projeto')
            elif not p.is_file(): errors.append(f'{prefix}.asset não existe: {asset}')
            elif p.suffix.lower() not in {'.png','.jpg','.jpeg','.webp','.svg'}:
                errors.append(f'{prefix}.asset deve ser imagem suportada: {asset}')
        click=s.get('click_target')
        if click:
            if s.get('kind')!='software': errors.append(f'{prefix}: clique permitido só em software')
            if i == len(scenes)-1: warnings.append(f'{prefix}: clique ignorado na última cena')
            if not all(isinstance(click.get(k),(int,float)) and 0<=click[k]<=1 for k in ('x','y')):
                errors.append(f'{prefix}.click_target x/y precisam estar entre 0 e 1')
            if not click.get('label'): errors.append(f'{prefix}.click_target.label obrigatório')
        if s.get('asset_status')=='placeholder':
            warnings.append(f'{prefix} usa placeholder: não publique como cena real da marca')
    total = len(scenes)*sum(v.get(k,0) for k in ('explain_seconds','focus_seconds','transition_seconds')) + v.get('cta_seconds',0)
    return obj,total,errors,warnings

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);a=p.parse_args()
    obj,total,errors,warnings=load(a.config)
    print(f'Cenas: {len(obj.get("scenes",[]))}; duração: {total:.2f}s')
    for msg in warnings:print('AVISO:',msg)
    for msg in errors:print('ERRO:',msg)
    if errors:sys.exit(1)
    print('Estrutura do projeto: OK')
