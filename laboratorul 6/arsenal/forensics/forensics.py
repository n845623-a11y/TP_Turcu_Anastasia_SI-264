"""Magic bytes, strings, EXIF/GPS si extragere ZIP dupa IEND."""
import argparse,json,re,struct,zipfile,io
from pathlib import Path
from PIL import Image,ExifTags

def tip_real(cale):
    with open(cale,'rb') as f: cap=f.read(8)
    for semn,nume in [(b'%PDF','pdf'),(b'\x89PNG\r\n\x1a\n','png'),(b'\xff\xd8','jpeg'),(b'PK\x03\x04','zip/docx')]:
        if cap.startswith(semn): return nume
    return cap.hex()

def grade(dms,emisfera):
    v=float(dms[0])+float(dms[1])/60+float(dms[2])/3600
    if isinstance(emisfera,bytes): emisfera=emisfera.decode()
    return -v if emisfera in ('S','W') else v

def metadate(cale):
    with Image.open(cale) as img:
        exif=img.getexif()
        rezultat={ExifTags.TAGS.get(k,str(k)):str(v) for k,v in exif.items() if k!=34853}
        gps=exif.get_ifd(34853) if 34853 in exif else {}
        if gps:
            rezultat['GPS']={'latitudine':grade(gps[2],gps[1]),'longitudine':grade(gps[4],gps[3])}
        return rezultat

def carve(cale,iesire):
    date=Path(cale).read_bytes()
    if not date.startswith(b'\x89PNG\r\n\x1a\n'): raise ValueError('Nu este PNG')
    poz=8
    while poz+12<=len(date):
        n=struct.unpack('>I',date[poz:poz+4])[0]
        tip=date[poz+4:poz+8]
        poz+=12+n
        if poz>len(date): raise ValueError('PNG trunchiat')
        if tip==b'IEND': break
    else: raise ValueError('IEND absent')
    i=date.find(b'PK\x03\x04',poz)
    if i<0: raise ValueError('ZIP absent dupa IEND')
    continut=date[i:]
    with zipfile.ZipFile(io.BytesIO(continut)) as z:
        if z.testzip(): raise ValueError('ZIP corupt')
        nume=z.namelist()
        secrete={n:z.read(n).decode('utf-8',errors='replace') for n in nume}
    Path(iesire).write_bytes(continut)
    return {'offset':i,'fisiere':nume,'continut':secrete}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--probe',default='probe')
    p.add_argument('--iesire',default='rezultate')
    a=p.parse_args(); probe=Path(a.probe); out=Path(a.iesire); out.mkdir(parents=True,exist_ok=True)
    rezultat={'tipuri':{n:tip_real(probe/n) for n in ['foto.jpg','ascuns.png']},
      'strings':[x.decode('ascii') for x in re.findall(rb'[ -~]{4,}',(probe/'ascuns.png').read_bytes())],
      'metadate':metadate(probe/'foto.jpg'),'arhiva':carve(probe/'ascuns.png',out/'gasit.zip')}
    (out/'forensics.json').write_text(json.dumps(rezultat,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'secret.txt').write_text(rezultat['arhiva']['continut']['secret.txt'],encoding='utf-8')
    print(json.dumps(rezultat,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
