# CNTS

CNTS predstavlja projekat koji služi za upravljanje _Counter Strike 1.6_ zadavanjem komandi pomoću:
* Ruke: Pucanje, promena oružja, punjenje municije, kupovina, ...
* Govora: Pozicioniranje nišana


## Članovi tima:

[Miloš Panić (sw19-2018)](https://github.com/panicmilos)  
[Luka Šerbedžija (sw32-2018)](https://github.com/lukaserbedzija)

## Resursi:

### Skupovi podataka:
* [Glasovni skup podataka](https://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html)
* [Originalni skup podataka ruke](https://drive.google.com/drive/u/0/folders/1Hj3N59H-WLxANH8zJPIwqeqQoomIj9FT)
* [Transformisani trening skup podataka ruke](https://drive.google.com/drive/u/4/folders/1AK69Apg3GPpM45lSbnmvg7-Fmi7KQW6T)
* [Transformisani test skup podataka ruke](https://drive.google.com/drive/u/4/folders/1QqaiqftelPoj8em5_2PyPU-zAZSt5J82)

<small>
Sve skupove podataka koji sadrže slike smo mi pravili.
Labela svake slike korespondira folderu u kojem se nalazi.
</small>

### Istrenirani modeli 
* [Naš model na skupu podataka](https://drive.google.com/drive/u/4/folders/1mDOZUibSGsfHMTZrDdq5aTkRW96sXQ9A)
* [VGG model na skupu podataka](https://drive.google.com/drive/u/4/folders/1Fzel9fw5Fkh9XlJzHg82-3mz9sa01--S)
* [Naš model na glasovnom skupu podataka](https://drive.google.com/drive/u/4/folders/1PHCroxWqK67dxM0qlqGx3FNtsQGjhFpE)

<small>
Glasovni skup podataka je isključivo treniran na našem modelu zato što VGG zahteva da broj kanala ulaza bude tri.
</small>

## Rezultati:

### Rezultati treniranja modela nad skupom slika:

Skup podataka je izdeljen u proporciji Trening, Validacioni, Test na: 75/15/10%

| Accuracy | Nad validacionim | Nad testnim  |
| :------: | :--------------: | :----------: |
| Naš      | 90.00%           | 96.00%       |
| VGG      | 92.00%           | 97.00%       |

### Rezultati treniranja modela nad glasovnim skupom:

_Accuracy_ nad glasovnim test skupom podataka iznosi 91.00%.

## Struktura
 ./
  * controller
    * cs.py - izvršava zadatu komandu uz dodatnu logiku timeout-a, baferovanja, ...
    * keyboard.py - sadrži funkcije za simulaciju pritiska dugmeta uz pomoć D_KEYS pošto je _Counter Strike 1.6_ pisan uz pomoć _DirectX_
    * mouse.py - sadrži funkcije za simulaciju klika i pokreta miša uz pomoć _pyautogui_
  * models - sadrži sve arhitekture modela
  * preprocessors
    * image.py - na osnovu zadate putanje učitava sve slike i povezuje ih sa labelama. Svakoj slici menja veličinu na 128x128 (najveća veličina sa kojom smo uspeli da istreniramo dataset)
    * sound.py - na osnovu zadate putanje učitava sve zvuke i povezuje ih sa labelama. Svaki zvuk limitira na jednu sekundu i reprezentuje ga kao _MFCC_
  * transformations - sadrži funkcije za rotate, flip iz crop koje su implementirane na osnovu _imgaug_. Extract metoda je implementirana uz pomoć binarnog thresholda sa gornjom i donjom granicom.
  * utils - sadrži funkcije za rad sa tredovima, timeoutom, os-om, ...

  Ostali fajlovi koji su opisani u sekciji "Korišćenje".

## Zavisnosti

Skoro sve potrebne zavisnosti se mogu instalirati uz pomoć komande `pip install -r requirements.txt`.

_PyAudio_ se mora instalirati uz pomoć sledećih [komandi](https://stackoverflow.com/a/70287202):

```
pip install pipwin
pipwin install pyaudio
```
ili uz pomoć npr. _conda_ alata.

## Korišćenje:

`dataset_generator.py` se pokreće komandom `python dataset_generator.py --args`.

 Pokretanjem ovog fajla se generiše dataset koji se nalazi na ulaznoj putanji uz pomoć rotate, flip, extract i crop transformacija i nakon toga se čuva na izlaznoj putanji u okviru dva foldera _train_ i _test_ čiji se odnos takođe zadaje.

| Argumenti   | Tip   | Značenje  | Inicijalna vrednost |
| :---------: | :---: | :--------------: | :----------: |
| input_path  | str   | Putanja do foldera sa originalnim skupom podataka | HandDataset |
| output_path | str   | Putanja do foldera gde će transformisan skup podataka biti sačuvan | generated_${currentTimestamp()} |
| test_split  | float | Procenat transformisanog skupa koji će biti korišćen za tesni | 0.1 |

`train.py` se pokreće komandom `python train.py --args`.

Pokretanjem ovog fajla se trenira željena arhitektura skupom podataka koji se nalazi na ulaznoj putanji i nakon toga se tako istrenirani model čuva na izlaznoj putanji.

| Argumenti         | Tip   | Značenje  | Inicijalna vrednost |
| :---------------: | :---: | :--------------: | :----------: |
| input_path        | str   | Putanja do foldera sa trening skupom podataka | datasets/train |
| model             | str   | Arhitektura modela. Može biti: 'custom_hands', 'custom_voice', 'vgg_hands' | custom_hands |
| model_output_path | str   | Putanja do foldera gde će istrenirani model biti sačuvan | trained_model |
| batch_size        | int   | Broj slika obrađenih u svakoj fazi treniranja | 32 |
| epochs            | int   | Broj epoha treniranja | 10 |
| validation_split  | float | Procenat trening skupa koji će biti korišćen za validaciju | 0.1 |

`test.py` se pokreće komandom `python test.py --args`.

Pokretanjem ovog fajla se testira trenirani model, čija se putanja zadaje, nad skupom podataka koji se nalazi na ulaznoj putanji i nakon toga se na izlaznom uređaju ispisuju loss i acc.

| Argumenti  | Tip   | Značenje  | Inicijalna vrednost |
| :--------: | :---: | :--------------: | :----------: |
| input_path | str   | Putanja do foldera sa testnim skupom podataka | datasets/test |
| resource   | str   | Tip resursa koji se testira: 'image', 'voice' | image |
| model_path | str   | Putanja do foldera gde je istrenirani model   | trained_model |
| batch_size | int   | Broj slika obrađenih u svakoj fazi testiranja | 128 |

`hand_detector.py` se pokreće komandom `python hand_detector.py --args`.

Pokretanjem ovog fajla kreće detekcija pokreta ruke uz pomoć _WebCam_. Pokret ruke se mora nalaziti u regionu od interesa. Klasifikacija pokreta se vrši uz pomoć treniranog modela čija se putanja zadaje.

| Argumenti      | Tip   | Značenje  | Inicijalna vrednost |
| :------------: | :---: | :--------------: | :----------: |
| model_path     | str   | Putanja do foldera sa treniranim modelom | trained_models/image |
| min_confidence | float | Najmanja vrednost sigurnosti predikcije kako bi se ona uzela kao tačnom | 0.5 |
| handle_action  | bool  | Primenjivanje akcije na Counter Strike 1.6   | True |
| roi_x          | int   | X kordinata regiona od interesa | 200 |
| roi_y          | int   | Y kordinata regiona od interesa | 200 |
| roi_width      | int   | Dužina regiona od interesa | 600 |
| roi_height     | int   | Širina regiona od interesa | 600 |

`voice_detector.py` se pokreće komandom `python voice_detector.py --args`.

Pokretanjem ovog fajla kreće detekcija glasa ili thresholda. Prilikom detekcije glasa, da bi se on smatrao aktivnošću, mora preći zadati prag nakon čega se pravi snimak dužine 1 sekundu nad kojim se radi klasifikacija. Klasifikacija glasovne komande se vrši uz pomoć treniranog modela čija se putanja zadaje.

| Argumenti       | Tip   | Značenje  | Inicijalna vrednost |
| :-------------: | :---: | :--------------: | :----------: |
| mode            | str   | Mod za detekciju glasa ili thresholda. Vrednosti: 'detect_voice' ili 'detect_threshold' | detect_voice |
| voice_threshold | float | Najmanja vrednost glasovne aktivnost | 0.015 |
| model_path      | str   | Putanja do foldera sa treniranim modelom   | trained_models/voice |
| min_confidence  | float | Najmanja vrednost sigurnosti predikcije kako bi se ona uzela kao tačnom | 0.5 |
| handle_action   | bool  | Primenjivanje akcije na Counter Strike 1.6   | True |


`play.py` se pokreće komandom `python play.py --args`.

Pokretanjem ovog fajla se pokreću detekcija pokreta ruke i glasa u posebnim nitima kako ne bi došlo do međusobnog blokiranja.

| Argumenti            | Tip   | Značenje  | Inicijalna vrednost |
| :------------------: | :---: | :--------------: | :----------: |
| image_model_path     | str   | Putanja do foldera sa treniranim modelom za slike | trained_models/image |
| image_min_confidence | float | Najmanja vrednost sigurnosti predikcije pokreta kako bi se ona uzela kao tačnom | 0.5 |
| roi_x                | int   | X kordinata regiona od interesa | 200 |
| roi_y                | int   | Y kordinata regiona od interesa | 200 |
| roi_width            | int   | Dužina regiona od interesa | 600 |
| roi_height           | int   | Širina regiona od interesa | 600 |
| voice_threshold      | float | Najmanja vrednost glasovne aktivnost | 0.015 |
| voice_model_path     | str   | Putanja do foldera sa treniranim modelom za glas   | trained_models/voice |
| voice_min_confidence | float | Najmanja vrednost sigurnosti predikcije glasovne komande kako bi se ona uzela kao tačnom | 0.5 |
