"""Steganografie RGB cu terminator nul si verificarea capacitatii."""
import argparse
from PIL import Image

def ascunde(sursa,destinatie,mesaj):
    date=mesaj.encode('utf-8')
    if b'\0' in date: raise ValueError('Mesajul contine terminator nul')
    with Image.open(sursa) as original: img=original.convert('RGB')
    biti=[(x>>t)&1 for x in date+b'\0' for t in range(7,-1,-1)]
    if len(biti)>img.width*img.height*3: raise ValueError('Capacitate insuficienta')
    canale=bytearray(img.tobytes())
    for i,bit in enumerate(biti): canale[i]=(canale[i]&254)|bit
    Image.frombytes('RGB',img.size,bytes(canale)).save(destinatie,format='PNG')

def dezvaluie(cale):
    with Image.open(cale) as img: canale=img.convert('RGB').tobytes()
    rezultat=bytearray()
    for i in range(0,len(canale)-7,8):
        octet=0
        for c in canale[i:i+8]: octet=(octet<<1)|(c&1)
        if octet==0: return rezultat.decode('utf-8')
        rezultat.append(octet)
    raise ValueError('Terminator absent')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='comanda',required=True)
    a=sub.add_parser('ascunde'); a.add_argument('sursa'); a.add_argument('destinatie'); a.add_argument('mesaj')
    b=sub.add_parser('dezvaluie'); b.add_argument('sursa')
    args=p.parse_args()
    if args.comanda=='ascunde':
        ascunde(args.sursa,args.destinatie,args.mesaj)
        print('Mesaj salvat:',dezvaluie(args.destinatie))
    else: print(dezvaluie(args.sursa))
if __name__=='__main__': main()
