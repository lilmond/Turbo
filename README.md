# Turbo
Turbo-charged mass port scanner. Scan 256 IP ports in just 1 second.

# Installation
For Linux platforms:
```
git clone https://github.com/lilmond/Turbo
cd ./Turbo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# System Installation
For Linux platform:
```
cp ./turbo.py /usr/bin/turbo
chmod 775 /usr/bin/turbo
```

# Usage
```
 ________                     __                 
|        \                   |  \                
 \$$$$$$$$__    __   ______  | $$____    ______  
   | $$  |  \  |  \ /      \ | $$    \  /      \ 
   | $$  | $$  | $$|  $$$$$$\| $$$$$$$\|  $$$$$$\
   | $$  | $$  | $$| $$   \$$| $$  | $$| $$  | $$
   | $$  | $$__/ $$| $$      | $$__/ $$| $$__/ $$
   | $$   \$$    $$| $$      | $$    $$ \$$    $$
    \$$    \$$$$$$  \$$       \$$$$$$$   \$$$$$$ 

     Source: https://github.com/lilmond/Turbo

     
usage: turbo.py [-h] -p PORT [--include-port] CIDR

Turbo-charged TCP port scanner.

positional arguments:
  CIDR                  IP CIDR, Example: 10.7.0.0/24

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to scan.
  --include-port        Include port in the output.
```

Please don't forget to leave a star and follow :3
