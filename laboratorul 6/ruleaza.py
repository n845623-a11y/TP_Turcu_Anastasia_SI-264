"""Reproduce laboratorul si pastreaza output-ul efectiv."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
comenzi=[['probe/pregateste.py'],['arsenal/forensics/decode.py','probe/mesaj.txt','--fisier','--iesire','arsenal/forensics/fisa.json'],
 ['arsenal/forensics/decode.py','probe/xor.bin','--fisier','--mod','xor','--iesire','rezultate/xor.json'],
 ['arsenal/forensics/decode.py','probe/hashuri.txt','--fisier','--mod','hash','--wordlist','probe/wordlist.txt','--iesire','rezultate/hashuri.json'],
 ['arsenal/forensics/forensics.py'],['arsenal/forensics/lsb.py','ascunde','probe/foto.jpg','stego.png','FLAG{ascuns_in_pixeli}'],
 ['arsenal/forensics/lsb.py','dezvaluie','stego.png'],['-m','pytest','teste','-v']]
(ROOT/'rezultate').mkdir(exist_ok=True)
with (ROOT/'rezultate/output.txt').open('w',encoding='utf-8') as log:
    for args in comenzi:
        r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',env={**__import__('os').environ,'PYTHONIOENCODING':'utf-8'})
        text='$ python '+' '.join(args)+'\n'+r.stdout+r.stderr+'\n'
        log.write(text); print(text)
        if r.returncode: raise SystemExit(r.returncode)
