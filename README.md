# TDK_2023
BCE 2023 Tudományos Diákköri Konferencia - Gárdi Réka

Az alkalmazás futtatásához a Python 3.8-as verzió szükséges, illetve a következő csomagok (verzió) telepítése:

matplotlib 3.2.2; 
pandas 1.5.3;
numpy 1.23.5;
sklearn 0.0.post1;
pandastable 0.13.0;
tkinter 8.6

A gmm_app.py megnyitása után futtatni kell a teljes kódot, és meg is nyílt a program. Az alkalmazás használati útmutatója TDK-dolgozatom VII. 3. 1. fejezetében található.
Két .csv fájl található még a repozitóriumban, amelyekkel ki lehet próbálni az alkalmazások működését. Az 'example-spontan-300.csv' esetében a mérés során egyáltalán nem történt ingerlés, de a mérésben voltak spontán aktív sejtek, így ezzel érdemes kipróbálni a véletlen erdő alkalmazást. Ez annyit jelent, hogy a mérést a modell továbbra is szétbontja két időszakra, és csak az első 300-on vizsgálja a spontán aktivitás jelenlétét. Az 'example-glu-300.csv' esetében pedig 300-nál történt ingerlő anyag beadás. A véletlen erdő modellben így egyik esetben sem kell az alapértelmezett vektor értékeket megváltoztatni az összevonáshoz. 
