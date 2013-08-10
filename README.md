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

The second configuration file is a SET (Social-Engineering Toolkit) local configuration file this way you can choose to use apache, modify listening ports, and other options during your automated web attacks.  

Note: If you select to use Java self signed certs within the attack the attack will not be successful due to more options need to be set within the SET setup.  This is in development and should be implemented shortly.

### 2.6 - EC2 AMI Image configuration
You need to configure a EC2 AMI image with metasploit, SET, apache2, and nmap and save it as an AMI image.  This is the base image that will be launched and terminated at the start and end of each attack.  The following outlines the steps I took to setup my own EC2 AMI image with Metasploit, SET, Nmap, and Apache2 installed and ready to go.

* Launch a new Ubuntu Server 12.04.2 LTS 32-bit instance within AWS EC2

 Note: This will be our base image we work off of, you can leave all the instance details and sizeing defaults for now and we can resize if need be within our config file and launch larger instances of our AMI image.  The only exception is to add a name for the instance in the tagging section.

* Next either create a new key pair or choose an existing keypair you already have.  

 Note: This will have to be local on your client system to be able to SSH into the system and allow cloudPWN to automatically setup the attacks.

* Next create a new Security Group and add at least the following ports, you can customize this to your liking this is my default SET security group within EC2:

 	* 21/tcp   0.0.0.0/0
 	* 22/tcp   0.0.0.0/0
 	* 53/tcp   0.0.0.0/0
 	* 80/tcp   0.0.0.0/0
 	* 443/tcp  0.0.0.0/0
 	* 8080/tcp 0.0.0.0/0
 	* 8081/tcp 0.0.0.0/0

 Note: These firewall rules will allow inbound traffic on all of the above ports from anywhere.

* Now that the instance is configured review and launch the instance. Once the instance is launched and running, ssh into the instance and follow the rest of this guide to install SET, Metasploit, Apache, and Nmap.

* git clone SET and install 

 	```bash
 	$ sudo apt-get update
	$ sudo apt-get upgrade
	$ sudo apt-get install git
	$ cd
	$ git clone https://github.com/trustedsec/social-engineer-toolkit.git
	$ cd social-engineer-toolkit/
	$ sudo python setup.py install
	$ cd
	```
* Install SET dependencies

	```bash
	$ wget 'http://corelabs.coresecurity.com/index.php?module=Wiki&action=attachment&type=tool&page=Impacket&file=impacket-0.9.9.9.tar.gz' -O impacket-0.9.9.9.tar.gz
	$ tar xzf impacket-0.9.9.9.tar.gz
	$ cd impacket
	$ sudo python setup.py install
	$ cd
	```

* Rename the set directory

	```bash
	$ sudo mv /usr/share/setoolkit/ /usr/share/set/
	```

* Install Metasploit and dependencies 
	
Note: Big Thanks to Carlos Perez for this tutorial http://www.darkoperator.com/installing-metasploit-in-ubunt/

 * Install Metasploit Dependencies

	```bash
	$ sudo apt-get install build-essential libreadline-dev  libssl-dev libpq5 libpq-dev libreadline5 libsqlite3-dev libpcap-dev openjdk-7-jre subversion git-core autoconf postgresql pgadmin3 curl zlib1g-dev libxml2-dev libxslt1-dev vncviewer libyaml-dev ruby1.9.3
	```
 * Install the requires gems for Metasploit

	```bash
		$ sudo gem install wirble sqlite3 bundler
	```
 * Install Nmap 

	```bash
	$ mkdir ~/tools
	$ cd ~/tools
	$ wget http://nmap.org/dist/nmap-6.25.tar.bz2
	$ tar jxf nmap-6.25.tar.bz2
	$ cd nmap-6.25/
	$ ./configure
	$ make
	$ sudo make install
	$ sudo make clean
	$ cd 
	```
 * Configure Postgresql

	Note: Make note of the password set for the msf user

	```bash
	$ sudo -s
	$ su postgres
	$ createuser msf -P -S -R -D
	$ createdb -O msf msf
	$ exit
	$ exit
	```
 * Install Metasploit

	```bash
	$ cd /opt
	$ sudo git clone https://github.com/rapid7/metasploit-framework.git
	$ cd metasploit-framework
	$ sudo bash -c 'for MSF in $(ls msf*); do ln -s /opt/metasploit-framework/$MSF /usr/local/bin/$MSF;done'
	$ bundle install
	```
 * Create the database.yml file

	```bash
	$ sudo vim /opt/metasploit-framework/database.yml
	```
	* Contents of the database.yml file

		```bash
		production:
   			adapter: postgresql
   			database: msf
   			username: msf
   			password: [enter msf db password here]
   			host: 127.0.0.1
   			port: 5432
   			pool: 75
   			timeout: 5
   		```
   		```bash
   		$ sudo sh -c "echo export MSF_DATABASE_CONFIG=/opt/metasploit-framework/database.yml >> /etc/profile"
		
		$ source /etc/profile
		```
 * Metasploit is installed and now launch msfconsole to make sure it is up and running

	```bash
	$ sudo msfconsole
	```
 * Edit the SET config file and tell it where Metasploit is installed

	```bash
	$ cd /usr/share/set
	$ sudo vim config/set_config
	```
	Note: change the metasploit directory to /opt/metasploit-framework/ within the SET config file.

 * Install Apache2 for SET Apache support

	```bash
	$ sudo apt-get install -f apache2 libapache2-mod-php5
	$ sudo update-rc.d apache2 disable
	$ sudo service apache2 stop
	```
 * Launch setoolkit and accept the agreement

	```bash
	$ sudo setoolkit
	```

 * Next in the EC2 dashboard under instances right click the configured instance and select Create Image (EBS image) and enter a unique name and description.

 * Once the Image is created and saved under AMIs expand the AMI image and copy the AMI ID

 * Next edit the cloudPWN configuration file and add the AMI ID to the image_list list

 * Now your custom SET and Metasploit AMI image is setup and ready to rock and roll ;) 

## 3.0 - The Future
### 3.1 - Future Development List

 * Add support for additional cloud/vps providers
 * Add self hosted support
 * Add Nmap module to launch multiple Nmap scans in multiple instances
 * Add Phishing email support and email lists for phishing and web attacks
 * Add Recon-ng support and automation
 * Add Recon-ng import to import and create email lists
