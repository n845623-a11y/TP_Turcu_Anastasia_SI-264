"""Decoder pentru probe locale de laborator."""
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote_to_bytes

def citibil(b):
    return bool(b) and all(32 <= c < 127 for c in b)

def ghici_strat(s):
    if re.search(r'%[0-9a-fA-F]{2}', s): return 'url'
    if s and len(s)%2 == 0 and re.fullmatch(r'[0-9a-fA-F]+',s): return 'hex'
    if s and len(s)%4 == 0 and re.fullmatch(r'[A-Za-z0-9+/]*={0,2}',s):
        try:
            base64.b64decode(s, validate=True)
            return 'base64'
        except ValueError: pass
    return 'necunoscut'

def desfa(s):
    strat=ghici_strat(s)
    if strat=='url': return strat,unquote_to_bytes(s)
    if strat=='hex': return strat,bytes.fromhex(s)
    if strat=='base64': return strat,base64.b64decode(s,validate=True)
    return strat,s.encode('utf-8')

def decodeaza(date, limita=8):
    curent=date
    pasi=[]
    vazute={date}
    for _ in range(limita):
        try: s=curent.decode('utf-8')
        except UnicodeDecodeError: break
        strat, nou=desfa(s)
        if strat=='necunoscut' or nou in vazute: break
        # Evita interpretarea unui text obisnuit drept base64 binar.
        if strat=='base64' and not citibil(nou):
            try: nou.decode('utf-8')
            except UnicodeDecodeError: break
            if not all(c.isprintable() or c.isspace() for c in nou.decode('utf-8')): break
        pasi.append({'strat':strat,'rezultat':nou.decode('utf-8',errors='replace')})
        curent=nou
        vazute.add(nou)
    return {'strat':pasi[0]['strat'] if pasi else 'necunoscut',
            'straturi':pasi,'rezultat':curent.decode('utf-8',errors='replace'),
            'rezultat_hex':curent.hex()}

def xor_candidati(date):
    rezultate=[]
    for k in range(256):
        clar=bytes(b^k for b in date)
        if citibil(clar):
            text=clar.decode('ascii')
            scor=sum(c.lower() in ' etaoinrsul' for c in text)/len(text)
            scor+=2 if 'FLAG{' in text else 0
            rezultate.append({'cheie':k,'rezultat':text,'scor':round(scor,4)})
    return sorted(rezultate,key=lambda x:x['scor'],reverse=True)

def sparge_hash(tinta, cuvinte):
    algoritm={32:'md5',40:'sha1',64:'sha256'}.get(len(tinta))
    if not algoritm or not re.fullmatch(r'[0-9a-fA-F]+',tinta):
        raise ValueError('Hash invalid sau lungime neacceptata')
    # Lungimea sugereaza algoritmul doar in cadrul acestor probe.
    for cuv in cuvinte:
        cuv=cuv.rstrip('\r\n')
        if hashlib.new(algoritm,cuv.encode('utf-8')).hexdigest()==tinta.lower():
            return {'algoritm':algoritm,'parola':cuv}
    return {'algoritm':algoritm,'parola':None}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('intrare')
    p.add_argument('--fisier',action='store_true')
    p.add_argument('--mod',choices=['decode','xor','hash'],default='decode')
    p.add_argument('--wordlist',default='probe/wordlist.txt')
    p.add_argument('--iesire',default='arsenal/forensics/fisa.json')
    a=p.parse_args()
    date=Path(a.intrare).read_bytes() if a.fisier else a.intrare.encode()
    if a.mod=='decode': rezultat=decodeaza(date.strip())
    elif a.mod=='xor': rezultat={'candidati':xor_candidati(date)}
    else:
        cuvinte=Path(a.wordlist).read_text(encoding='utf-8').splitlines()
        rezultat={'hashuri':[dict(hash=h,**sparge_hash(h,cuvinte)) for h in date.decode().splitlines() if h]}
    destinatie=Path(a.iesire)
    destinatie.parent.mkdir(parents=True,exist_ok=True)
    destinatie.write_text(json.dumps(rezultat,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(rezultat,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
