# SpecializationProject

File structure (files not in this structure are either helper files or not in use/not finished):
```
SpecializationProject/
├── datasets/                       # Datasets for solar traces
|   ├── autumn.tsv
│   ├── summer.tsv
│   └── vinter.tsv
├── modules/                        # All necessary modules for the design
|   ├── tests/                      # Test code for det different modules
│   |   ├── BT_test.py
│   |   ├── file_handler_test.py
│   |   ├── LED_test.py
│   |   └── SPI_test.py
│   ├── BT.py
│   ├── file_handler.py
│   ├── LED.py
│   ├── pinOut.py
│   └── SPI.py
├── main.py
├── messages.py
├── parameters.py
├── .gitignore
├── README.md
└── requirements.txt
```


# How to install and use:
Install pigpio:
```
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
cd ..
```
Clone Github repository to Desktop, move into it, and install requirements:
```
cd Desktop
git clone https://github.com/sindrekvande/SpecializationProject
cd https://github.com/sindrekvande/SpecializationProject
pip3 install -r requirements.txt
```
Start the pigpio Deamon:
```
sudo pigpiod
```
Set the desired parameters in the parameters.py file, before you run the program:
```
python3 main.py
```