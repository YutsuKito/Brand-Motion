"""Gera trilha instrumental original ou apenas cliques sincronizados, sem downloads."""
import math, wave
from pathlib import Path
import numpy as np


def generate_audio(output: Path, duration: float, clicks: list[float], original_music: bool=True, sample_rate: int=44100):
    output=Path(output)
    sr=sample_rate
    n=int(math.ceil(sr*duration))
    y=np.zeros(n,dtype=np.float32)
    rng=np.random.default_rng(22027)
    def add(t, signal,vol=1.):
        idx=int(round(t*sr))
        if idx<0 or idx>=n:return
        signal=np.asarray(signal,dtype=np.float32)
        amt=min(len(signal),n-idx)
        y[idx:idx+amt]+=signal[:amt]*vol
    if original_music:
        bpm=122;beat=60/bpm
        chord_roots=[(110.,[220.,261.63,329.63]),(87.3,[174.61,220.,261.63]),(65.4,[130.81,164.81,196.]),(98.,[196.,246.94,293.66])]
        for bar in range(int(duration/(4*beat))+2):
            time=bar*4*beat
            bass,chord=chord_roots[(bar//2)%4]
            tt=np.arange(int(sr*4*beat),dtype=np.float64)/sr
            env=np.minimum(1,tt/.18)*np.clip((4*beat-tt)/.3,0,1)
            audio=sum(np.sin(2*np.pi*f*tt) for f in chord)/3
            add(time,audio*env,.046)
        for i in range(int(duration/beat)+3):
            time=i*beat
            tt=np.arange(int(sr*.22))/sr
            phase=2*np.pi*(56*tt+70*(1-np.exp(-tt*24))/24)
            kick=np.sin(phase)*np.exp(-tt*24)
            add(time,kick,.22)
            tx=np.arange(int(sr*.06))/sr
            noise=rng.normal(0,1,len(tx))
            hat=np.diff(np.r_[noise[0],noise])*np.exp(-tx*50)
            add(time,hat,.011)
            add(time+beat*.5,hat,.013)
            if i%4 in (1,3):
                sn=rng.normal(0,1,len(tt))*np.exp(-tt*24)
                add(time,sn,.038)
            base=chord_roots[(i//8)%4][0]
            tb=np.arange(int(sr*.28))/sr
            add(time,(np.sin(2*np.pi*base*tb)*np.exp(-tb*11)),.07)
    for t in clicks:
        tt=np.arange(int(sr*.13))/sr
        noise=rng.normal(0,1,len(tt))
        sound=(np.sin(2*np.pi*1850*tt)*.35+np.sin(2*np.pi*910*tt)*.23+noise*.14)*np.exp(-tt*54)
        add(t,sound,.41)
    if original_music:
        fadein=np.clip(np.arange(n)/(sr*.45),0,1)
        fadeout=np.clip((n-np.arange(n))/(sr*1.2),0,1)
        y*=fadein*fadeout
    else:
        y*=.95
    peak=float(np.max(np.abs(y))) if len(y) else 0
    if peak>.86:y*=.86/peak
    pcm=(np.clip(y,-1,1)*32767).astype(np.int16)
    output.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(output),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
    return output
