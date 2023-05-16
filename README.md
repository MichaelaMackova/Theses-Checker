# Nástroj pro kontrolu diplomových prací

### Autor: Michaela Macková ([xmacko13@stud.fit.vutbr.cz](mailto:xmacko13@stud.fit.vutbr.cz))
### Vedoucí: Ing. Tomáš Milet, Ph.D.
---





## O aplikacích

Vytvořené aplikace realizují nástroj, který kontroluje (převážně typografické) chyby, které se často vyskytují v diplomových pracích.
Součástí této práce byly vytvořeny dvě aplikace, jedna webová a druhá spustitelná v příkazovém řádku. Obě aplikace byly vytvořeny v jazyce Python a pro zpracování PDF dokumentu používají knihovnu [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/).

<br>

**Webový nástroj**

Vytvořená webová aplikace je volně dostupná na webové stránce [https://theseschecker.eu.pythonanywhere.com/](https://theseschecker.eu.pythonanywhere.com/).

Vstupem této aplikace je PDF soubor obsahující kontrolovanou technickou zprávu. Výstupem je poté tento soubor doplněný o grafické označení nalezených chyb.  Upravený PDF soubor je poté zobrazen přímo na webové stránce. Chyby jsou označeny PDF anotacemi.


<br>

**Program pro použití v příkazovém řádku**

Vstupem této aplikace je jeden či více PDF souborů, kde každý obsahuje kontrolovanou technickou zprávu. Pomocí dostupných přepínačů lze nastavit, které kontroly se provedou a zda budou při kontrolách vnořené PDF soubory (nacházející se uvnitř PDF dokumentu) brány jako obrázky. Výstupem jsou poté tyto PDF dokumenty doplněny o grafické označení nalezených chyb. Chyby jsou označeny PDF anotacemi.





---

## Instalace závislostí

Před spuštěním programu je nutné si nainstalovat všechny balíčky, na kterých je aplikace závislá. Pro ulehčení tohoto instalování byly vytvořeny soubory 
se sepsanými balíčky a jejich verzemi, které mohou být použity s příkazem `pip install`. Tyto soubory jsou uloženy ve složce `src\`. Obě vytvořené verze aplikace Theses Checker (webový nástroj i program do příkazového řádku) byly vyvinuty v programovacím jazyku **Python ve verzi 3.10**.
Jiné verze nebyly vyzkoušeny.


<br>

**Webový nástroj**

Instalace závislostí pro *webový nástroj* se provede následujícím příkazem: 
```
pip install -r requirements_web.txt
```


<br>

**Program pro použití v příkazovém řádku**

Instalace závislostí pro *program v příkazovém řádku* se provede následujícím příkazem: 
```
pip install -r requirements.txt
```





---

## Nastavení před prvním použitím
Po nainstalování závislostí je před prvním použitím obou aplikací nutné provést pár úprav.

<br>

**Webový nástroj**

Pro správnou funkci webové aplikace je nutné, aby soubor `theses_checker.py` byl umístěn ve složce `src\web\theses_checker\bl\` (v této složce je původně umístěn). Dále by se měl před zveřejněním této aplikace nastavit tajný klíč, který je uveden v souboru `.env`. Na tomto paměťovém médiu je v tomto souboru uvedena základní hodnota tajného klíče, tato hodnota se však pro udržení bezpečnosti musí ručně změnit. Tento tajný klíč lze vygenerovat například na stránce [Djecrety](https://djecrety.ir/). Dále se musí nastavit proměnná `DEBUG`, která se vyskytuje v souboru `settings.py`. Touto proměnnou lze určit, zda aplikace bude pracovat v módu pro vývoj, či v módu pro produkci. (V módu pro produkci nemusí na lokálním serveru fungovat statické soubory, jako jsou například `style.css` a `script.js`.)


<br>

**Program pro použití v příkazovém řádku**

Pro správnou funkci programu, který je používán v příkazovém řádku, je nutné, aby soubor `theses_checker.py` byl umístěn ve stejné složce, ve které se nachází i soubor `check.py`. Původní složka tohoto souboru `check.py` je `src\` a soubor `theses_checker.py` se původně nachází ve složce `src\web\theses_checker\bl\`.





---

## Použití

**Webový nástroj**

Server pro webový nástroj se spouští příkazem:
```
python manage.py runserver
```

Dále je webová aplikace dostupná na webové stránce [Theses Checker](https://theseschecker.eu.pythonanywhere.com/).


<br>

**Program pro použití v příkazovém řádku**

Tento program se spouští následovně:

```
python check.py [PREPINAC]… in_file [in_file]…
```

Přepínače, které lze použít, jsou: 
+ -h nebo --help
+ --embedded_PDF
+ -o nebo --overflow
+ -i nebo --image_width
+ -H nebo --Hyphen
+ -t nebo --TOC
+ -s nebo --space_bracket
+ -e nebo --empty_chapter
+ -b nebo --bad_reference

Aplikaci lze použít například následovně:

```
python check.py -h
```

```
python check.py file.pdf
```

```
python check.py file1.pdf file2.pdf file3.pdf
```

```
python check.py -o -t file.pdf file2.pdf
```

```
python check.py file.pdf -H -s -b
```



---

## Struktura paměťového média

Toto paměťové médium obsahuje složky:
+ appendices – Obsahuje odpovědi k dotazníkům, plakát a vytvořené demonstrační video
+ dataset – Obsahuje soubory, na kterých byly hledány časté chyby a na kterých byla testována vytvořená aplikace
+ latex – Zdrojové kódy (a ostatní potřebné soubory) textu této bakalářské práce 
+ src – Zdrojové kódy k vytvořeným programům
    + web – Zdrojové kódy pro webovou aplikaci
        + files – Složka pro výstupní PDF 
        + static – Obsahuje všechny statické soubory
        + templates – Obsahuje všechny šablony webových stránek
        + theses_checker – Zdrojové kódy pro webový modul Theses Checker
        + web – Zdrojové kódy pro nastavení webu
+ thesis – Obsahuje text této bakalářské práce ve formátu PDF

<br>

Toto je přesnější popis obsahu, ve kterém jsou uvedeny některé důležité soubory: 
```
├── appendices
│   ├── poster.pdf
│   ├── questionnaire_responses.xlsx
│   └── video.mp4
├── dataset
├── latex
├── src
│   ├── web
│   │   ├── files
│   │   ├── static
│   │   │   ├── css
│   │   │   └── js
│   │   ├── templates
│   │   ├── theses_checker
│   │   │   ├── bl
│   │   │   │   └── theses_checker.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── web
│   │   │   └── settings.py
│   │   ├── .env
│   │   └── manage.py
│   ├── check.py
│   ├── LICENSE
│   ├── requirements.txt
│   └── requirements_web.txt
├── thesis
│   └── xmacko13-Kontrola-diplomovych-praci.pdf
└── README.md
```




---