import os
import random
import time
import threading
import hashlib
import numpy as np
from Crypto.Hash import RIPEMD160
from cryptofuzz import Convertor
from cryptofuzz.assest import MAX_PRIVATE_KEY
from colorthon import Colors
from numba import cuda

# Initialize Converter and Colors
co = Convertor()

# Define Colors
RED = Colors.RED
GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
CYAN = Colors.CYAN
WHITE = Colors.WHITE
RESET = Colors.RESET

# Set up CUDA parameters for your current setup
threads_per_block = 256
num_keys = 100000

# Function to clear console
def getClear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Key Generation Function
def KeyGen(size):
    k = "".join(random.choice('0123456789abcdef') for _ in range(size))
    if int(k, 16) < MAX_PRIVATE_KEY:
        return k
    else:
        return KeyGen(size)

# Convert hex to address
def Hex_To_Addr(hexed, compress):
    return co.hex_to_addr(hexed, compress)

# Load Rich Addresses from File
def Rich_Loader(FileName):
    return set([i.strip() for i in open(FileName).readlines()])

# Display the Header
def getHeader(richFile, loads, found):
    getClear()
    output = f"""
{YELLOW}\t██████╗ ██╗   ██╗██████╗  ██████╗ ███╗   ███╗██╗██████╗ {RESET}
{YELLOW}\t██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗████╗ ████║██║██╔══██╗{RESET}
{YELLOW}\t██████╔╝ ╚████╔╝ ██████╔╝██║   ██║██╔████╔██║██║██║  ██║{RESET}
{YELLOW}\t██╔═══╝   ╚██╔╝  ██╔══██╗██║   ██║██║╚██╔╝██║██║██║  ██║{RESET}
{YELLOW}\t██║        ██║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║██████╔╝{RESET}
{YELLOW}\t╚═╝        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═════╝ {RESET}
{RED}╔═╗╦═╗╔═╗╔═╗╦═╗╔═╗╔╦╗╔╦╗╔═╗╦═╗{RESET}  {WHITE}╔╦╗╔╦╗╔╦╗╦═╗╔═╗╔═╗ ╔═╗╔═╗╔╦╗{RESET}
{RED}╠═╝╠╦╝║ ║║ ╦╠╦╝╠═╣║║║║║║╣ ╠╦╝{RESET}  {WHITE}║║║║║║ ║║╠╦╝╔═╝╠═╣ ║  ║ ║║║║{RESET}
{RED}╩  ╩╚═╚═╝╚═╝╩╚═╩ ╩╩ ╩╩ ╩╚═╝╩╚═{RESET}  {WHITE}╩ ╩╩ ╩═╩╝╩╚═╚═╝╩ ╩o╚═╝╚═╝╩ ╩{RESET}
{RED}➜{RESET} {WHITE}Pyromid {RESET}{CYAN}v2 {RESET}Ⓟ{GREEN} Powered By CryptoFuzz - Exclusive MMDRZA.COM{RESET}
{RED}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Import Rich File :{RESET}{CYAN} {richFile}                {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Method Generated :{RESET}{CYAN} Random Without Repeat.    {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Address Type     :{RESET}{CYAN} Compressed / Uncompressed.{RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Max Decimal (HEX):{RESET}{CYAN} {MAX_PRIVATE_KEY}         {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Result Checked   :{RESET}{CYAN} {loads}                   {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Matched Address  :{RESET}{CYAN} {found}                   {RESET}
"""
    print(output)

# CUDA Kernel for Key Generation and Address Checking
@cuda.jit
def check_keys(keys, results):
    idx = cuda.grid(1)
    if idx < len(keys):
        private_key = keys[idx]
        # Simulate conversion and checking logic
        # For simplicity, just save the private key in the result
        results[idx] = int(private_key, 16)  # Simulate some result

# Main Function to Check Keys
def MainCheck():
    global z, wf
    target_file = 'Rich.txt'
    Targets = Rich_Loader(target_file)
    z = 0
    wf = 0
    lg = 0
    getHeader(richFile=target_file, loads=lg, found=wf)
    
    keys = []
    while len(keys) < num_keys:
        keys.append(KeyGen(64))

    keys_device = cuda.to_device(np.array(keys))
    results_device = cuda.device_array_like(keys_device)

    check_keys[num_keys // threads_per_block, threads_per_block](keys_device, results_device)
    results = results_device.copy_to_host()

    for i in range(num_keys):
        z += 1
        privatekey = keys[i]
        result = results[i]
        
        # Simulate finding a match (this would be your actual match logic)
        if result % 2 == 0:  # Simulate a found condition
            wf += 1
            open('Found.txt', 'a').write(f"Address: {result}\n"
                                         f"Private Key: {privatekey}\n"
                                         f"DEC: {int(privatekey, 16)}\n"
                                         f"{'-' * 66}\n")
        elif int(z % 100000) == 0:
            lg += 100000
            getHeader(richFile=target_file, loads=lg, found=wf)
            print(f"Generated: {lg} (SHA-256 - HEX) ...")
        else:
            lct = time.localtime()
            tm = time.strftime("%Y-%m-%d %H:%M:%S", lct)
            print(f"[{tm}][Total: {z} Check: {z * 2}] #Found: {wf} ", end="\r")

if __name__ == '__main__':
    t = threading.Thread(target=MainCheck)
    t.start()
    t.join()
