#!/bin/bash

# This install was run on Proxmox Ubuntu 18.10

apt update
apt upgrade -y

dpkg-reconfigure locales

apt install -y git
apt install -y python3-dev python3-pip
apt install -y python3-enchant libaspell-dev

wget https://raw.githubusercontent.com/sopel-irc/sopel/master/requirements.txt
pip3 install -r requirements.txt
rm requirements.txt
wget https://raw.githubusercontent.com/sopel-irc/sopel/master/dev-requirements.txt
pip3 install -r dev-requirements.txt
rm dev-requirements.txt
wget https://raw.githubusercontent.com/SpiceBot/SpiceBot/development/Installation%20Files/requirements.txt
pip3 install -r requirements.txt
rm requirements.txt
pip3 install sopel

mkdir /usr/local/lib/python3.6/dist-packages/sopel/modules/stock
mv /usr/local/lib/python3.6/dist-packages/sopel/modules/* /usr/local/lib/python3.6/dist-packages/sopel/modules/stock/

useradd sopel
passwd sopel
mkdir /home/sopel
chown sopel:sopel /home/sopel
usermod -aG sudo sopel

git clone https://github.com/SpiceBot/SpiceBot.git /home/sopel/SpiceBot
cd /home/sopel/SpiceBot
git checkout dev

mkdir /run/sopel
echo $$ > /run/sopel/sopel-SpiceBotSERV.pid
chmod -R 777 /run/sopel/

apt install mysql-server libmysqlclient-dev -y
pip3 install mysql


cp /home/sopel/SpiceBot/System-Files/Config/SpiceBot.cfg /home/sopel/SpiceBot.cfg
cp /home/sopel/SpiceBot/System-Files/systemd/SpiceBot.service /lib/systemd/system/SpiceBot.service
systemctl enable SpiceBot.service
