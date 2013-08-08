# cloudPWN v0.1 (development)

Author: J. David Bressler (@bostonlink), GuidePoint Security LLC.<br/>
cloudPWN - Automating Attacks within the cloud

## 1.0 - About
TODO

## 2.0 - Requirements and Installation

### 2.1 - Supported Platforms
cloudPWN has been tested and is supported on Mac OS X and Kali Linux.

### 2.2 - Requirements
cloudPWN is supported and tested on Python 2.7.3

### 2.3 - Python dependencies

```bash
$ sudo easy_install fabric
$ sudo easy_install boto
```

### 2.4 - Installation
To install there is nothing to it other than installing the python dependencies and git cloning the repo.

```bash
$ git clone https://github.com/bostonlink/cloudPWN.git
```

### 2.5 - Configuration Files
There are several configuration files within cloudPWN currently.  First configuration file in config/cloudPWN.conf is the core configuration file to cloudPWN and holds all data needed by the tool.  The most important part of setting up cloudPWN is to assure the right amazon AWS API keys and SSH keys are added to the configuration file without these cloudPWN will not work.

The second configuration file is a SET (Social-Engineering Toolkit) local configuration file this way you can choose to use apache, listening ports, and other options during your automated web attacks.  

Note: If you select to use Java self signed certs within the attack the attack will not be successful due to more options need to be set within the SET setup.  This is in development and should be implemented shortly.

### 2.6 - EC2 AMI Image configuration
You need to configure a EC2 AMI image with metasploit, SET, apache2, and nmap and save it as an AMI image.  This is the base image that will be launched and terminated at the start and end of each attack.  The following outlines the steps I took to setup my own EC2 AMI image with Metasploit, SET, Nmap, and Apache2 installed and ready to go.

 * Launch a new Ubuntu Server 12.04.2 LTS 32-bit instance within AWS EC2

 Note: This will be our base image we work off of, you can leave all the instance details and sizeing defaults for now and we can resize if need be within our config file and launch larger instances of our AMI image.  The only exception is to add a name for the instance in the tagging section.

 * Next either create a new key pair or choose an existing keypair you already have.  

 Note: This will have to be local on your client system to be able to SSH into the system and allow cloudPWN to automatically setup the attacks.

 * Next create a new Security Group and add at least the following ports, you can customize this to your liking this is my default SET security group within EC2:
 ** 21/tcp   0.0.0.0/0
 ** 22/tcp   0.0.0.0/0
 ** 53/tcp   0.0.0.0/0
 ** 80/tcp   0.0.0.0/0
 ** 443/tcp  0.0.0.0/0
 ** 8080/tcp 0.0.0.0/0
 ** 8081/tcp 0.0.0.0/0

 Note: These firewall rules will allow inbound traffic on all of the above ports from anywhere.

 * 



All Done!!  Happy Hunting!