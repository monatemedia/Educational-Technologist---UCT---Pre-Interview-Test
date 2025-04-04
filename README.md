# Educational Technologist - UCT - Pre-Interview Test


---

### **Section 1**

#### **1. The “Capture Agent” is used to record the video and audio, please name the devices or connections that are used as input sources.**

- Sony NX3 Camera (SDI)
    
- Mic and Lapel Mic (XLR/SDI)
    
- Rifle Mic (XLR/USB)
    
- Presentation PC (HDMI)
    
- Laptop, iPad (HDMI/CAT 6E/HDMI)
    
- Network Connection (Ethernet for Opencast integration)
    

#### **2. The “Presentation PC” is used by a person to show a presentation that will be recorded with the video and audio. What kind of hardware and software configuration would you recommend?**

- **Hardware:**
    
    - Modern PC with at least Intel i3+ / AMD Ryzen 3+
        
    - 8GB RAM or more
        
    - 128GB SSD storage or more for fast performance
        
    - HDMI output for external display
        
    - Gigabit PCI Express Network Adapter
        
    - USB ports X 4 or more
        

- **Software:**
    
    - Windows 11 or Linux (Kubuntu/Mint Cinnamon Edition)
        
    - Web browser
        
    - Microsoft PowerPoint / LibreOffice Impress
        
    - VLC Media Player
        
    - Any other specific presentation software required by faculty
        

#### **3. What kind of hardware would you recommend for the “Capture Agent”?**


- **Hardware:**
    
    - Modern PC with at least Intel i7+ / AMD Ryzen 7+
        
    - 32GB RAM or more
        
    - 1TB+ NVMe SSD storage for fast performance
        
	- Dedicated GPU (NVIDIA GeForce RTX 3060 or AMD Radeon RX 6600) for video rendering
	    
    - VisionLC-HD2 Dual Channel "LiveStream:Capture" Card for HDMI input
        
    - VisionLC-SDI Single Channel "LiveStream:Capture" Card for SDI input
        
    - Gigabit PCI Express Network Adapter  for Opencast integration
        
    - USB ports X 4 or more
        

#### **4. Why would there be 2 microphones used in this configuration?**

- One microphone may be used for the presenter, while the other is used for audience interaction (Q&A).
    
- It ensures redundancy in case one microphone fails.
    
- It allows for separate audio channels for better mixing and clarity.
    

#### **5. Explain why an SDI cable is used between the Capture Agent and the Camera?**

- SDI (Serial Digital Interface) supports higher-quality video transmission than HDMI.
    
- It allows longer cable runs without signal degradation (100m VS 3m for HDMI).
    
- It supports embedded audio and timecode, reducing cable clutter and capturing additional data.
    
- It provides a secure twist-lock locking mechanism for professional setups.
    
- It carries high-quality uncompressed video signals
    
- It's more reliable in professional settings compared to consumer alternatives
    

#### **6. The PT-752 and PT-751 takes an HDMI signal as input and converts it to CAT, why would this be required in this setup?**

- CAT (Ethernet cable) allows for long-distance transmission of HDMI signals.
    
- It reduces signal degradation compared to long HDMI cables.
    
- It is cost-effective and easier to install in large venues.
    

#### **7. What is the difference between Stereo and Mono signal?**

- **Stereo is a two-channel audio source, and Mono is a single-channel audio source.**
    

#### **8. From the diagram what future enhancement/automation/improvements would you recommend be implemented?**

- Remove [VA-1DVIN](https://www.avshop.ca/video/accessories/kramer-va-1dvin-dvi-edid-emulator) from the venue as it is not required to connect a laptop or iPad to the `Capture Agent`.
    
- Plug the `Presentation PC` into the `PDU`. There are power points available.
    
- Move the `Rifle Mic` and `Shure X2U` from the `Capture Agent` to the `Presentation PC` making it easy for the presenter to talk through their presentation from the `Presentation PC` desk.
    
- Install a USB cable between the `Capture Agent` and the `DSP` to be able to record audio from the `Mic` and `Lapel Mic` without using the `Sony NX3` if video is not required. The `Capture Agent` and the `DSP` sit in the same rack.
    
- Replace the `10m USB extension` with a USB cable of >3m, if the devices at the end of it can be moved closer. Alternatively, if the devices cannot be moved closer, implement a [Active USB Cable](https://www.takealot.com/usb-2-0-active-extension-cable-10m/PLID44484002?srsltid=AfmBOooizpj5UAPOSmaY7XWEtaA9cLJk35ZL5b2MIzcs1kJvcwHhuLH4) or [USB-to-Ethernet Extenders](https://www.takealot.com/usb-to-ethernet-adapter-usb-to-ethernet-extension/PLID72477084) with CAT 6E cable solution if that is not possible. This assumes that this cable is in fact required.
    
- Unplug the `Keyboard and Mouse` from the `USB HUB` and plug it directly into the `Capture Agent`.
    
- Find out if we can fit a PDU to the camera to be able to turn it on and off as needed..
    
- Automate the lights in the room using the PDU via scheduling software, motion control or mobile apps.
    
- Integrate AI-based noise reduction for clearer audio.
    
- Use wireless microphones for better mobility.
    
- Implement cloud storage for automatic backup of the Capture Agent.
    
- Introduce remote monitoring and control via a web dashboard.
    

---

### **Section 2**

#### **1. Which Linux commands would you use to do the following?**

| Action                                                                       | Command                                                                                                                                                             |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| List the version number of the Operating System                              | `cat /etc/os-release` or `lsb_release -a`                                                                                                                           |
| Find all files containing a particular string in a folder                    | `grep -r "search_string" /path/to/folder`                                                                                                                           |
| Find all files starting with “sed” in a folder                               | `find /path/to/folder -name "sed*"`                                                                                                                                 |
| Determine the total size of a folder and all the files it contains           | `du -sh /path/to/folder`                                                                                                                                            |
| Determine which process running on the server is allocated a particular port | `sudo lsof -i :port_number` or `netstat -tulnp`                                                                                                                     |
| List the devices connected to the PC which has a particular name             | `lsusb \| grep "Device_Name"` for USB;<br>`lspci \| grep "Device_Name"` for PCI;<br>`lsblk \| grep "name"` for storage;<br>`hwinfo \| grep "name"` for all hardware |

#### **2. Which folder in Linux would you normally find…?**

| Description                                                                | Folder          |
| -------------------------------------------------------------------------- | --------------- |
| Log files for programs installed on the PC                                 | `/var/log`      |
| The web pages which are made available by web servers like Apache or Nginx | `/var/www/html` |
| The devices attached to the PC                                             | `/dev`          |

---

### **Section 3**
#### **Using any programming language, write a script to read in a text file containing a list of server names, ping each one, and if they do not respond, write those out to a file called “error.log”.**

##### Description

`pingy.py` is a Python script designed to check the connectivity of multiple servers using three different methods:

1. **DNS Lookup**: Verifies if the server’s domain can be resolved via DNS.
    
2. **HTTP(S) Check**: Confirms if the server responds to HTTP/HTTPS requests.
    
3. **Ping Test**: Pings the server to check if it is reachable via ICMP.
    

The script supports two ways to specify the servers:

- **Command-line arguments**: You can pass server addresses directly.
    
- **Text file**: You can provide a `.txt` file (e.g., `servers.txt`) containing a list of servers to check. If no `.txt` file is provided, the script will look for `servers.txt` in the same folder. A test `servers.txt` file is provided for testing.
    

The script then generates a summary report on the connectivity status of the servers, saving any unreachable servers into an `error.log` file.

##### Features

- Supports DNS, HTTP, and Ping checks for server connectivity.
    
- Allows checking servers via command-line arguments or from a `.txt` file.
    
- Generates an `error.log` file with the list of unreachable servers.
    
- Easy-to-use and flexible, perfect for monitoring multiple servers.
    

##### How to Download

You can download the `pingy.py` script from the GitHub repository:

1. Visit the repository page: [Educational-Technologist---UCT---Pre-Interview-Test](https://github.com/monatemedia/Educational-Technologist---UCT---Pre-Interview-Test)
    
2. Clone or download the repository using the following Git command:
    
    ```bash
    git clone https://github.com/monatemedia/Educational-Technologist---UCT---Pre-Interview-Test.git
    ```
    
    Or you can download the ZIP file from the GitHub page.
    

##### How to Use

###### Prerequisites

Ensure you have Python installed on your system. You can check this by running:

```bash
python --version
```

If Python is not installed, download and install the latest version from [python.org](https://www.python.org/downloads/).

###### Running the Script

1. Navigate to the directory where `pingy.py` is located.
    
2. To check connectivity for servers from the provided `servers.txt` file, use the following command:
    
    ```bash
    python pingy.py
    ```

3. To check connectivity for servers from any other `.txt` file, use the following command:
    
    ```bash
    python pingy.py <path_to_your_txt_file>
    ```
    
    For example:
    
    ```bash
    python pingy.py my_servers.txt
    ```
    
3. To check connectivity for servers directly passed as arguments, use:
    
    ```bash
    python pingy.py server1.com server2.com
    ```
    

##### Example

To use a custom file `my_servers.txt` to check server connectivity, run:

```bash
python pingy.py my_servers.txt
```

Alternatively, to pass servers directly from the command line:

```bash
python pingy.py example.com example2.com
```

##### Output

- The script will check each server and print the status of DNS lookup, HTTP check, and Ping test to the terminal.
    
- The summary of the server statuses will be printed in the terminal.
    
- Any unreachable servers will be written to an `error.log` file in the same directory. If all servers respond, an empty `error.log` file will be created.
    

