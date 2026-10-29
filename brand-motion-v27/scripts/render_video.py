#!/usr/bin/env python3
"""Brand Motion V27: screenshots determinísticos -> storyboard, WAV e MP4."""
import argparse,json,math,shutil,subprocess,sys,base64,mimetypes
from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from validate_project import load
from audio import generate_audio

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'engine'/'composition.html').resolve()

def source_uris(data,root):
    # Dados embutidos evitam file:// bloqueado, políticas de rede e assets quebrados.
    result=json.loads(json.dumps(data))
    def as_data(asset):
        path=(root/asset).resolve()
        if not path.is_relative_to(root): raise ValueError('Asset fora do projeto: '+str(asset))
        mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
    for scene in result['scenes']:
        scene['asset']=as_data(scene['asset'])
    if result['brand'].get('logo'):
        result['brand']['logo']=as_data(result['brand']['logo'])
    return result

def make_board(images,output):
    if not images:return
    width=480;height=270
    columns=min(3,len(images));rows=math.ceil(len(images)/columns)
    board=Image.new('RGB',(columns*width,rows*(height+37)),'#f7f8fa')
    d=ImageDraw.Draw(board)
    for i,(label,img) in enumerate(images):
        x=(i%columns)*width;y=(i//columns)*(height+37)
        with Image.open(img) as im:
            im=im.convert('RGB');im.thumbnail((width,height),Image.Resampling.LANCZOS)
            board.paste(im,(x+(width-im.width)//2,y))
        d.text((x+14,y+height+7),label[:58],fill='#18243d')
    board.save(output,quality=90)

def run():
    ap=argparse.ArgumentParser()
    ap.add_argument('--config',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--preview-only',action='store_true')
    ap.add_argument('--resume',action='store_true',help='aproveitar quadros existentes do MESMO manifest')
    ap.add_argument('--allow-placeholders',action='store_true',help='permite exportar demonstração sintética')
    ap.add_argument('--max-frames',type=int,default=None,help='teste parcial de renderização')
    ap.add_argument('--music',type=Path,help='faixa licenciada fornecida pelo usuário')
    args=ap.parse_args()
    config=args.config.resolve();out=args.output.resolve()
    data,total,errors,warnings=load(config)
    if errors:raise SystemExit('Erros:\n'+'\n'.join(errors))
    for w in warnings:print('AVISO:',w)
    if any(s.get('asset_status')=='placeholder' for s in data['scenes']) and not(args.preview_only or args.allow_placeholders):
        raise SystemExit('Há imagens de placeholder. Troque por assets reais ou use --allow-placeholders para teste.')
    out.mkdir(parents=True,exist_ok=True)
    v=data['video'];fps=v['fps'];width=v['width'];height=v['height']
    if (width,height)!=(1920,1080):raise SystemExit('Template genérico foi dimensionado para 1920x1080')
    scene_len=v['explain_seconds']+v['focus_seconds']+v['transition_seconds']
    full_frames=round(total*fps)
    frame_count=min(full_frames,args.max_frames) if args.max_frames else full_frames
    if frame_count <=0:raise SystemExit('max-frames deve ser positivo')
    timeline=[];clicks=[]
    for i,s in enumerate(data['scenes']):
        start=i*scene_len
        evt={'scene':i+1,'label':s['label'],'start':round(start,3),'explanation_end':round(start+v['explain_seconds'],3),
             'focus_end':round(start+v['explain_seconds']+v['focus_seconds'],3),'end':round(start+scene_len,3)}
        if s.get('click_target') and i<len(data['scenes'])-1:
            tm=start+v['explain_seconds']+v['focus_seconds']+.5
            evt['click_at']=round(tm,3);evt['click_label']=s['click_target']['label'];clicks.append(tm)
        timeline.append(evt)
    timeline.append({'cta_start':round(len(data['scenes'])*scene_len,3),'cta_end':round(total,3)})
    (out/'timeline.json').write_text(json.dumps(timeline,indent=2,ensure_ascii=False),encoding='utf-8')
    resolved=source_uris(data,config.parent)
    previews=[]
    print('Composição:',len(data['scenes']),'cenas,',round(total,2),'segundos,',full_frames,'frames')
    with sync_playwright() as p:
        chromium = Path(p.chromium.executable_path)
        system_browser = next((shutil.which(name) for name in ('chromium','chromium-browser','google-chrome','google-chrome-stable') if shutil.which(name)),None)
        exe = str(chromium) if chromium.is_file() else system_browser
        if not exe: raise SystemExit('Chromium não encontrado. Execute: python -m playwright install chromium')
        b=p.chromium.launch(headless=True,executable_path=exe,args=['--disable-dev-shm-usage'])
        page=b.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        page.set_content(HTML.read_text(encoding='utf-8'),wait_until='load')
        page.evaluate('(data)=>window.initProject(data)',resolved)
        page.evaluate('document.fonts.ready')
        page.evaluate('async () => { await Promise.all([...document.images].filter(i=>i.src).map(i=>i.complete?Promise.resolve():new Promise(r=>{i.onload=r;i.onerror=r}))); }')
        preview_times=[]
        for i,s in enumerate(data['scenes']):
            base=i*scene_len
            preview_times.append((s['label']+' • explicação',base+min(2.,v['explain_seconds']-.1)))
            preview_times.append((s['label']+' • zoom',base+v['explain_seconds']+v['focus_seconds']/2))
        preview_times.append(('CTA',len(data['scenes'])*scene_len+v['cta_seconds']*.65))
        for j,(label,tt) in enumerate(preview_times):
            page.evaluate('(t)=>window.seek(t)',tt)
            target=out/f'preview_{j:02}.jpg'
            page.screenshot(path=str(target),type='jpeg',quality=86,animations='disabled')
            previews.append((label,target))
            state=page.evaluate('window.frameState')
            if state['phase']=='focus':
                cx=state['center']['x'];cy=state['center']['y']
                # center of target transform must be exact geometric center
                if abs(cx-width/2)>0.01 or abs(cy-height/2)>0.01:
                    raise RuntimeError(f'Centro fora do alvo no frame {tt}: {cx},{cy}')
        make_board(previews,out/'storyboard.jpg')
        if not args.preview_only:
            frames=out/'frames';frames.mkdir(exist_ok=True)
            for frame in range(frame_count):
                framepath=frames/f'{frame:05d}.jpg'
                if args.resume and framepath.is_file(): continue
                page.evaluate('(t)=>window.seek(t)',frame/fps)
                page.screenshot(path=str(framepath),type='jpeg',quality=88,animations='disabled',caret='hide')
                if frame%150==0:print('Quadro:',frame,'/',frame_count,flush=True)
        b.close()
    if args.preview_only:
        print('Prévia:',out/'storyboard.jpg');return
    wav=out/'track.wav'
    music_mode=v.get('music','original')
    generate_audio(wav,total,clicks,original_music=(music_mode!='silent' and not args.music))
    source=str(out/'frames'/'%05d.jpg')
    mp4=out/'final.mp4'
    cmd=['ffmpeg','-y','-v','error','-framerate',str(fps),'-i',source]
    if args.music:
        if not args.music.is_file():raise SystemExit(f'Música não encontrada: {args.music}')
        cmd+=['-stream_loop','-1','-i',str(args.music.resolve()),'-i',str(wav)]
        cmd+=['-filter_complex',f'[1:a]volume=0.24[b];[b][2:a]amix=inputs=2:duration=first,atrim=duration={frame_count/fps:.3f}[mixed]','-map','0:v:0','-map','[mixed]']
    else:
        cmd+=['-i',str(wav)]
        cmd+=['-map','0:v:0','-map','1:a:0']
    cmd+=['-t',f'{frame_count/fps:.3f}','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(mp4)]
    print('Exportando MP4...')
    subprocess.run(cmd,check=True)
    print('MP4:',mp4)
    print('Story:',out/'storyboard.jpg')
    if frame_count==full_frames:
        subprocess.run([sys.executable,str(ROOT/'scripts'/'qa.py'),'--video',str(mp4),'--config',str(config)],check=True)
    else:print('Render parcial de teste: QA completo ignorado.')

if __name__=='__main__':run()
