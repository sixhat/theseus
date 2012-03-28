#!/bin/bash

cd /home/admin/theobservatorium.eu/www/Theseus

#./html2text.sh ElPais
#./html2text.sh LeMonde
#./html2text.sh Publico
#./html2text.sh PublicoImpresso
#./html2text.sh guardian.co.uk
#./html2text.sh nol.hu
#./html2text.sh theaustralian.com.au

./j2zip.sh ElPais
./j2zip.sh LeMonde
./j2zip.sh Publico
./j2zip.sh PublicoImpresso
./j2zip.sh guardian.co.uk
./j2zip.sh nol.hu
./j2zip.sh theaustralian.com.au
./j2zip.sh jornaldenegocios.pt


mv ElPais/*.zip ../dados/
mv LeMonde/*.zip ../dados/
mv Publico/*.zip ../dados/
mv PublicoImpresso/*.zip ../dados/
mv guardian.co.uk/*.zip ../dados/
mv nol.hu/*.zip ../dados/
mv theaustralian.com.au/*.zip ../dados/
mv jornaldenegocios.pt/*.zip ../dados/
