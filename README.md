# NJ Hálózati címelemző

## Hallgató
Nagy János (NJ)

## Feladat leírása
Grafikus, offline Python-alkalmazás hálózati címek vizsgálatára. IPv4 vagy IPv6 cím és prefix megadásával megjeleníti a hálózati címet, maszkot, címtartományt, címszámot és címtípust. IPv4 esetén a broadcast címet is kiírja. Az eredmény JSON-fájlba menthető. A program nem csatlakozik hálózati eszközökhöz, és nem végez hálózati felderítést.

## Indítás
Python 3.10 vagy újabb, Tk támogatással. Külső pip-csomag nem szükséges.

Windows: a Python telepítőben legyen engedélyezve a Tcl/Tk összetevő és a Python PATH-hoz adása. A kicsomagolt mappában indítsd az `Inditas.bat` fájlt, vagy terminálban futtasd:

```
py main.py
```

A `main.py` és az `nj_halozat.py` maradjon ugyanabban a mappában.
Linuxon a Tk külön rendszerkomponens lehet (Debian/Ubuntu: python3-tk); az indítás `python3 main.py`.

## Használat
1. Írj be egy címet, például `192.168.1.10/24`.
2. Nyomd meg az Entert, vagy kattints az Elemzés gombra.
3. Olvasd le a táblázat eredményét.
4. A JSON mentése gombbal mentsd az eredményt.
5. A Törlés gomb üríti a bevitelt és az eredményt.

További példák: `10.0.0.5/255.255.255.0`, `192.168.1.0/31`, `2001:db8::1/64`.
Prefix nélkül a cím egyetlen címből álló /32 vagy /128 hálózatot jelent.

## Modulok és használt függvények
| Modul | Szerep | Használt függvények, elemek |
| --- | --- | --- |
| tkinter | Tanult grafikus modul | Tk(), StringVar(), mainloop(), bind() |
| tkinter.ttk | Grafikus vezérlők | Style(), Frame(), Label(), Entry(), Button(), Treeview(), Scrollbar() |
| tkinter.messagebox | Üzenetablakok | showerror(), showinfo() |
| tkinter.filedialog | Mentési hely kiválasztása | asksaveasfilename() |
| ipaddress | Bemutatandó modul | ip_interface(), ip_network(), ip_address() |
| json | Fájlba mentés | dump() |
| nj_halozat | Saját modul | nj_elemzes(), NJHalozat.nj_vizsgal(), NJHalozat.nj_torol() |

Az `ipaddress` három függvénye ténylegesen lefut az elemzéskor: az `ip_interface()` az IP-címet és prefixét értelmezi; az `ip_network(..., strict=False)` a hozzá tartozó hálózatot állítja elő; az `ip_address()` önálló címobjektumot hoz létre a cím tulajdonságainak vizsgálatához.

## Osztályok és saját függvények
- `NJHalozat`: az elemzés eredményét tároló saját osztály. `nj_vizsgal(cim)` elemzést végez; `nj_torol()` törli a tárolt eredményt.
- `NJAlkalmazas`: a grafikus felület saját osztálya. `nj_futtat()` az elemzés eseménykezelője, `nj_torol()` üríti a felületet, `nj_ment()` menti az adatokat.
- `nj_elemzes(cim)`: saját függvény, szótárban adja vissza az eredményeket.
- A konstruktorok (`__init__`) a Python által előírt nevű speciális metódusok.

## Működési tudnivalók
IPv4 /31 esetén mindkét cím, /32 esetén az egyetlen cím használható. IPv6 esetén nincs broadcast; a program /127 alatt kihagyja a hálózati alapcímet a használható tartományból, /127 és /128 esetén minden címet számol. A címszám elméleti tartományméret, nem a ténylegesen kiosztott vagy elérhető eszközök száma. A Privát/Globális/Speciális jelzés a Python `ipaddress` modul osztályozását követi; a Privát nem kizárólag az RFC1918 tartományokat jelöli. A program nem sorolja fel egyenként a címeket, így nagy IPv6-hálózatnál sem készít óriási listát.

## Követelmények és beadás
Az indítófájl `main.py`, az alapablak változója `root`, a program objektuma `app`. A saját modul, függvények és osztályok nevében szerepel az NJ monogram. A Python-kódban nincsenek kommentek. Eseménykezelés: gombnyomás és Enter billentyű.

GitHubra a `main.py`, `nj_halozat.py`, `Inditas.bat` és `README.md` fájlokat kell feltölteni. A repository linkjét Teamsben kell megosztani.

## Rövid bemutatási vázlat
Először a `main.py` létrehozza az ablakot és az alkalmazást. Elemzéskor az eseménykezelő meghívja az NJHalozat objektumot. Ez a saját modul nj_elemzes függvényére bízza a cím értelmezését. A függvény az ipaddress modul három függvényét használja, majd szótárat ad vissza. Az alkalmazás a szótárat táblázatban mutatja meg. Hibás címnél hibaüzenet jelenik meg; mentéskor a json.dump írja fájlba az eredményt.
