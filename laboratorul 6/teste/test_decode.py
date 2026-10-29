import hashlib,tempfile,unittest
from pathlib import Path
from PIL import Image
from arsenal.forensics.decode import desfa,ghici_strat,decodeaza,xor_candidati,sparge_hash
from arsenal.forensics.lsb import ascunde,dezvaluie
from arsenal.forensics.forensics import grade,tip_real

class TestDecode(unittest.TestCase):
    def test_base64(self):
        strat,b=desfa('U2FsdXQ=')
        self.assertEqual(strat,'base64'); self.assertEqual(b,b'Salut')
    def test_hex_url(self):
        self.assertEqual(ghici_strat('48656c6c6f'),'hex')
        self.assertEqual(desfa('%2Fetc'),('url',b'/etc'))
    def test_straturi(self):
        r=decodeaza(b'NTM1OTU3NTk=')
        self.assertEqual(r['rezultat'],'SYWY')
        self.assertEqual([p['strat'] for p in r['straturi']],['base64','hex'])
    def test_xor(self):
        clar=b'FLAG{test_xor}'
        self.assertEqual(xor_candidati(bytes(x^73 for x in clar))[0]['cheie'],73)
    def test_hash(self):
        for alg in ['md5','sha1','sha256']:
            h=hashlib.new(alg,b'parola').hexdigest()
            self.assertEqual(sparge_hash(h,['altceva','parola'])['parola'],'parola')
        self.assertIsNone(sparge_hash(hashlib.md5(b'x').hexdigest(),['y'])['parola'])
    def test_intrari(self):
        self.assertEqual(ghici_strat(''),'necunoscut')
        self.assertEqual(decodeaza(b'Salut lume!')['rezultat'],'Salut lume!')
        with self.assertRaises(ValueError): sparge_hash('abc',[])
    def test_lsb(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/'a.png'; b=Path(t)/'b.png'
            Image.new('RGB',(32,32),(100,110,120)).save(a)
            ascunde(a,b,'Mesaj cu ă și ț')
            self.assertEqual(dezvaluie(b),'Mesaj cu ă și ț')
            self.assertEqual(tip_real(b),'png')
            with self.assertRaises(ValueError): ascunde(a,b,'x'*1000)
            with self.assertRaises(ValueError): ascunde(a,b,'a\0b')
    def test_gps(self):
        self.assertAlmostEqual(grade((47,1,12),'N'),47.02)
        self.assertEqual(grade((28,30,0),'W'),-28.5)
if __name__=='__main__': unittest.main()
