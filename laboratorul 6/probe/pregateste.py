"""Probe demonstrative proprii, nu scriptul original al disciplinei."""
import base64, hashlib, io, zipfile
from pathlib import Path
from PIL import Image
from PIL.TiffImagePlugin import IFDRational
from urllib.parse import quote

def main():
    p=Path(__file__).resolve().parent
    mesaj='FLAG{straturile_au_fost_decodate}'
    cod=quote(base64.b64encode(mesaj.encode().hex().encode()).decode(),safe='')
    # Fortam un strat URL vizibil chiar daca base64 nu are padding.
    cod='%'+format(ord(cod[0]),'02X')+cod[1:]
    (p/'mesaj.txt').write_text(cod,encoding='ascii')
    (p/'xor.bin').write_bytes(bytes(b^73 for b in b'FLAG{xor_cu_cheia_73}'))
    parole=['laborator6','parola123','securitate']
    (p/'wordlist.txt').write_text('\n'.join(['admin','test',*parole,'student'])+'\n',encoding='utf-8')
    (p/'hashuri.txt').write_text('\n'.join(hashlib.new(a,w.encode()).hexdigest() for a,w in zip(['md5','sha1','sha256'],parole))+'\n')
    img=Image.new('RGB',(320,240))
    img.putdata([((x*3+y)%256,(y*2+x)%256,(x+y*3)%256) for y in range(240) for x in range(320)])
    exif=Image.Exif()
    exif[271]='Laborator demonstrativ'
    exif[272]='Camera virtuala'
    exif[306]='2026:10:20 12:00:00'
    exif[34853]={1:'N',2:(IFDRational(47),IFDRational(1),IFDRational(12)),3:'E',4:(IFDRational(28),IFDRational(49),IFDRational(48))}
    img.save(p/'foto.jpg',exif=exif)
    buf=io.BytesIO()
    img.save(buf,format='PNG')
    arh=io.BytesIO()
    with zipfile.ZipFile(arh,'w',compression=zipfile.ZIP_STORED) as z:
        z.writestr('secret.txt','FLAG{arhiva_ascunsa_la_coada}\n')
    (p/'ascuns.png').write_bytes(buf.getvalue()+arh.getvalue())
    print('Probe generate in',p)
if __name__=='__main__': main()
