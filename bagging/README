安裝最新版本 libmodbus5
`$ sudo apt-get install libmodbus5 libmodbus-dev`

編譯程式 `cc -o Hiwin_API Hiwin_API.c -lmodbus -I./`

生成so檔 `cc -fPIC -shared -o Hiwin_API.so Hiwin_API.c -lmodbus -I./`

執行 `python3 Hiwin_API_test.py`

/************ P.S. ************/

如需安裝其他版(請查閱)  [https://libmodbus.org/releases/](https://libmodbus.org/releases/)

`libmodbus-3.1.7`->更換成新版本

$ wget http://libmodbus.org/site_media/build/libmodbus-3.1.7.tar.gz

$ sudo chmod 755 libmodbus-3.1.7.tar.gz

$ tar zxvf libmodbus-3.1.7.tar.gz -C .

$ cd libmodbus-3.1.7/

$ ./configure

$ make

$ sudo make install

於此即完成安裝。
