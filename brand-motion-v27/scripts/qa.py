#!/usr/bin/env python3
"""Validação técnica de MP4 exportado (não substitui revisão humana/visual)."""
import argparse,json,math,subprocess,sys
from pathlib import Path
from validate_project import load

def run():
    p=argparse.ArgumentParser();p.add_argument('--video',type=Path,required=True);p.add_argument('--config',type=Path,required=True);a=p.parse_args()
    data,total,errors,warnings=load(a.config)
    if errors:raise SystemExit(str(errors))
    v=data['video'];flags=[]
    result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames','-of','json',str(a.video)],capture_output=True,text=True,check=True)
    meta=json.loads(result.stdout)
    streams=meta['streams'];vid=next((x for x in streams if x.get('codec_type')=='video'),None)
    aud=next((x for x in streams if x.get('codec_type')=='audio'),None)
    if not vid:flags.append('stream de vídeo ausente')
    else:
        if (vid.get('width'),vid.get('height'))!=(v['width'],v['height']):flags.append('resolução incorreta')
        if vid.get('codec_name')!='h264':flags.append('codec de vídeo diferente de H.264')
        n,d=(int(x) for x in vid['avg_frame_rate'].split('/'))
        if abs(n/d-v['fps'])>0.005:flags.append('FPS incorreto')
        if vid.get('nb_frames') and int(vid['nb_frames'])!=round(total*v['fps']):flags.append('contagem de quadros incorreta')
    if not aud:flags.append('faixa de áudio ausente')
    elif aud.get('codec_name')!='aac':flags.append('codec de áudio diferente de AAC')
    if abs(float(meta['format']['duration'])-total)>.06:flags.append('duração incorreta')
    dec=subprocess.run(['ffmpeg','-v','error','-i',str(a.video),'-f','null','-'],capture_output=True,text=True)
    if dec.returncode!=0:flags.append('falha na decodificação: '+dec.stderr[:350])
    report={'video':str(a.video.resolve()),'planned_duration':round(total,3),'actual_duration':float(meta['format']['duration']),
        'dimensions':[v['width'],v['height']],'fps':v['fps'],'frame_count':vid.get('nb_frames') if vid else None,
        'codec_video':vid.get('codec_name') if vid else None,'codec_audio':aud.get('codec_name') if aud else None,
        'decoder_ok':dec.returncode==0,'errors':flags,
        'notes':['Testes semânticos de clique e direitos de imagem exigem inspeção humana.','A planilha de licenças e os placeholders devem ser auditados antes de publicar.']}
    outfile=a.video.with_suffix('.qa.json');outfile.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print('QA:', 'APROVADO técnico' if not flags else 'FALHOU','|',outfile)
    for msg in flags:print('ERRO:',msg)
    if flags:sys.exit(1)
if __name__=='__main__':run()
