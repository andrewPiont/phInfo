---
layout: default
title: Raspberry Pi Content Server
---
[![CircleCI](https://circleci.com/gh/alexKleider/phInfo.svg?style=svg)](https://circleci.com/gh/alexKleider/phInfo)
# The Raspberry Pi as a Content Server

## Introduction

This directory hierarchy attempts to provide all that is needed
(information and support files) to make a `Raspberry Pi` into a
content server running a static content site as well as a
`Pathagar Book Server` suitable for classroom or library use.
Since `Raspbian`, the default `Raspberry Pi` `OS`, is `Debian`
based, these instructions (with modifications discussed in the
text) should be applicable to any other `Debian` based system.

The goal is to end up with a device that provides:

* the Pathagar Book Server, and 
* one or more static sites.

## The Process

The process is divided up into the following steps, the first
three of which are specific to the `Raspberry Pi`. The fifth
assumes a hardware set up similar to that of the `Raspberry Pi`
and will likely have to be modified considerably if using an
alternate server platform:

    * Raspberry Pi Acquisition
    * SD Card Preparation
    * Initial RPi Configuration (`raspi-config`)
    * OS Update and Installation of Utilities
    * Network Setup
    * Bring in Dependencies
    * Server Setup
    * Static Content
    * Pathagar Book Server
    * Add Another Static Content Site

### Raspberry Pi

The [Vilros basic starter kit](https://www.amazon.com/Vilros-Raspberry-Basic-Starter-Kit/dp/B01D92SSX6/ref=sr_1_4?s=pc&ie=UTF8&qid=1478455788&sr=1-4&keywords=raspberry+pi)
is recommended since it includes the required power cord, and a
protective case. WiFi is built in to this newer (v3) model
`Raspberry Pi`. The older (v2) model will work but a separate
[USB WiFi dongle](https://www.amazon.com/CanaKit-Raspberry-Wireless-Adapter-Dongle/dp/B00GFAN498/ref=sr_1_1?s=pc&ie=UTF8&qid=1486968857&sr=1-1&keywords=CanaKit+WIFI)
must be added.

### SD Card Preparation

A high capacity Micro SD [Card](https://www.amazon.com/SanDisk-microSDXC-Standard-Packaging-SDSQUNC-064G-GN6MA/dp/B010Q588D4/ref=sr_1_1?ie=UTF8&qid=1488675440&sr=8-1&keywords=64+gig+micro+sd+card)
is recommended<sup>[1](#1sdcard)</sup> and **RASPBIAN JESSIE LITE** 
is the recommended 
[image](https://www.raspberrypi.org/downloads/raspbian/)
to use.  While at the ``raspbian`` download site, it would be a
good idea to make a copy of the ``sha1sum`` shown below the
``Download ZIP`` button.  If you don't know the concept of a
``checksum`` or ``hash`` then you could forget all about this
without much risk of endangering your project. 

NOTE: The recent change from jessie to stretch is rumoured to 
have brocken a lot of systems so it might be better to stick with
jessie-lite available
[here](http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2017-07-05/).
The commands provided below take all of this into consideration so
you needn't worry about any of this.  

The following assumes you have a micro SD card as well as a card
reader which will work with your GNU/Linux computer. An Apple will
probably work the same but if your OS is by MicroSoft, you'll have
to look for instructions on the internet.

Unequivocally establish the `device name` your computer assigns
to the SD card and then unmount any of the possibly auto-mounted
volumes associated with this device. (A google search will
provide further information on how to do this.) We'll assume the
device is `/dev/sdb`; substitute as appropriate.  Getting this wrong
can be hazardous!!

Change into a directory where the image can be downloaded and then
unzipped.  It can eventually be deleted from your personal machine
so which directory you use doesn't much matter. Creating a new
empty directory for this purpose might make things less confusing.

        mkdir <newly_created_dirctory>
        cd <newly_created_dirctory>
        wget http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2017-07-05/2017-07-05-raspbian-jessie-lite.zip
        wget http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2017-07-05/2017-07-05-raspbian-jessie-lite.zip.sha1
        sha1sum 2017-07-05-raspbian-jessie-lite.zip.sha1 >> 2017-07-05-raspbian-jessie-lite.zip.sha1
        cat 2017-07-05-raspbian-jessie-lite.zip.sha1

The last command should result in two lines, both showing the same
sha1sum providing assurance that you have an unadulterated copy of
the image.  Assuming it is so and after you are positive that your
SD card is mounted at `/dev/sdb` or what ever device name you specify
in its place, continue with the following commands:

        unzip 2017-07-05-raspbian-jessie-lite.zip
        sudo dd if='2017-07-05-raspbian-jessie-lite.img' of=/dev/sdb bs=4M
        sudo sync

Now the SD card is ready for your Raspberry Pi and, if you wish,
the raspbian image can now be delete.  The following sequence of 
commands will remove the whole newly created directory from your
personal machine (if you wish to do so.)

        cd -
        rm -rf <newly_created_dirctory>

### Initial RPi Configuration (`raspi-config`)

Unfortunately `raspbian` is not shipped with the `ssh server` active
by default and for this reason the `Pi` must be run the first time
with a screen and keyboard attached.  Be sure the micro SD card is
securely inserted.  Having an ethernet cable connected is not
essential at this stage but could be helpful for trouble shooting.

At the beginning of power up you'll briefly see a message that the
root file system is being resized.  (When it acutally gets resized
is not clear to me because resizing comes up again later at the end
of `raspi-config`.)

Log on as user `pi` with password `raspberry` and then run:
        
        sudo raspi-config

As its name implies, this allows you to configure the Pi to suit
your needs. Make selections by using the up and down arrow keys
and once your choice is highlighted, use the left and right arrow
keys to pick `<Select>` (or `<Finish>`).  Here is an outline of what
is recommended or appropriate (at least for my use case):

    1. Change user password: I've been changing the pw to `pi::root` 
    2. Hostname: I suggest `rpi` (something short)
    3. Boot options:
        We are not installing a GUI so select B1 (boot into the
        command line interface) following which you will be given
        another list of options and again select B1 (log in
        required.)
    4. Localization Options:
        11 Change Locale: The default is `en_gb.UTF-8`: suitable
            for Great Britain.  For the American locale, scroll down
            (with the down arrow) until encountering the asterix (*)
            next to `en_gb.UTF-8`, toggle with the space bar, and
            then continue scrolling down until coming to
            `en_us.UTF-8`.  Toggle with the space bar again so the
            asterix appears. Here the behaviour of the interface is
            a bit different: the `Enter` key moves you forward to
            the next panel where you again use the down arrow
            to land on `en_us.UTF-8`.  Use the right arrow and then
            `Enter` over the `<Ok>`.
        Choose option 4 again.
        12 Change Time Zone: US, New Pacific
        13 Change Keyboard Layout: 
            generic 105-key (the default) seems to work
            I chose `Other` rather than the default
            (`English (UK)') and then select 'English (US)'
            There's no reason to change any of the remaining
            defaults.
    5. Interfacing Options:
        Only the second option is relevant to us:
        P2 SSH: Enable ssh server
        Be sure to select <Yes>, this is very important.
    6. Overclock: Left in the default state.
    7. Advanced options:
        A1 Expand file system: This is also very important.
        None of the other advance options concern us.
    8. Update this tool to latest version
        Optional: depends on internet connectivity
    9. About raspi-config

If you are connected by ethernet cable to the internet, it might
be worth checking connectivity:

        ping 8.8.8.8

Quit by using `^C` (Control C.)

Once done go ahead and shutdown:

        sudo shutdown -h now

Since its `SSH Server` is now activate, the `Raspberry Pi`
can be run `headless'.  Be sure it is connected to the internet
and powered up.  Determine its IP address <sup>[2](#2arpscan)</sup>
and then use your personal computer to log on remotely:

        ssh pi@<IPAddress>

When using SSH, following a shutdown or a reboot, the client
teminal sometimes freezes up.  This can be remedied with the
following 3 key strokes: Enter (the `Enter key`), tilde (`~`),
period (`.`).


### OS Update and Installation of Utilities

Be sure your platform (the `Raspberry Pi` or otherwise) is
connected to the internet.  After logging on as user
`pi`<sup>[3](#3username)</sup> using your newly set password,
(as described in the end of the last section)
update using the following command (which you can expect to
take a long time:)

        sudo apt-get -y update && sudo apt-get -y upgrade

The following sequence of commands ensures that you are in the
current user's home directory (`/home/pi`,) installs `git` and
then clones the phInfo repository<sup>[4](#4reponame)</sup>:

        cd
        sudo apt-get -y install git 
        git clone https://github.com/alexKleider/phInfo.git
        cd phInfo

This brings in the `phInfo` file hierarchy containing this
`README` as well as required scripts and files. The final
command puts you into that (`phInfo`) directory.

There are a number of utilities and customizations that are not
essential but I find them useful to have so my practice is to
also run the following script:

        ./favourites.sh



##### Network Setup

Network configuration is dependent on the hardware being used.
These instructions assume that there is an ethernet (eth0) port
and either a built in wifi or a usb wifi dongle as is true for
the Raspberry Pi. The instructions provided will have to be
modified if this is not your use case.
Configuration is done by commands in the networking.sh and the
iptables.sh scripts. There must be a reboot between the two.
But before beginning have a look through the initial
comments in `networking.sh`; you will probably want to edit
some of the files mentioned.

        # Edit networking.sh
        ./networking.sh
        # Wait a few minutes for the reboot before loging on again.
        cd phInfo
        ./iptables.sh

The last command again ends with a reboot.  If you end up with a
frozen terminal, try the following sequence of (3) key strokes:
`enter`, `~`, `.`

Even if you are not using a `Raspberry Pi`, it would probably be 
wise to look through the above two scripts so see what is being
done so you can get an idea what might be needed on your platform.

##### Bring in dependencies

The next script will take a long time (so be patient!) Near the end
you are three times asked to set a `MySQL` "root" password. Each
time leave it blank- do this by hitting the down arrow so that
`<Ok>` is highlighted and then hit `Enter`.
The script ends with a reboot.

        cd phInfo
        sudo ./dependencies.sh

### Server Setup

Log on again, `cd` into the project directory (`phInfo`) and then
have a look through the initial comments in `create-server.sh`.
Once you've finished editing to suit your own use case,
go ahead and run the script:

        cd phInfo
        # edit create-server.sh
        ./create-server.sh

Wait for a few minutes for your server (in my case it's the `Pi`) to
reboot and then test by connecting your wifi to the server. Once your
machine is connected to the server's wifi access point, pointing
your browser to `library.lan` should take you to the pathagar home
page.  Pointing to `rachel.lan` should take you to the static content.

### Static Content

To add your own static content simply copy the appropriate
`index.html` file together with any other supporting files to the
`/var/www/static/` directory, thus replacing the test page.

If your content is available on an ext4 formatted USB device with
LABEL=Static, (and you haven't modified the `create-server.sh` code,)
the following will serve as a template for the copy command:

        rsync -av /mnt/Static/<dir-containing-content>/ /var/www/static/

Note that the final slash(`/`) at the end of the first parameter to
`rsync` is important (so that only the content, not the directory
itself, gets copied. Presence or absence of the final slash in 
the second parameter is immaterial.)

If your content is at the top level of the medium you've mounted
(rather than inside its own directory) then change the command to
the following:

        rsync -av /mnt/Static/* /var/www/static/

If your server is the `Raspberry Pi` set up as described here,
then entering "rachel.lan" in the URL window of a browser running
on a wifi client machine will result in your content being displayed.


### Pathagar Book Server

Choose a database password consisting of alphanumerics, dashes and
underscores but no other special characters. Make a record of it
somewhere so as to be sure not to forget it. Then log on to your
`Raspberry Pi` as user `pi` and run the following command after
first substituting your chosen password inside the single quotes:

        export MYSQL_PASSWORD='db-password'

You will also later need a pathagar superuser password so now would
be a good time to pick one and record it somewhere.  I suggest
'ph-su-pw'.

The next sequence of commands brings in Pathagar, carries out
necessary configurations, activates the virtual environment so that
a superuser can be created and then deactivates the environment since
if all goes well you won't need it any longer.  Django arranges for
its activation when needed.  The `pip install -r requirements.pip`
command in `pathagar-setup.sh` takes a very long time so be patient.

        cd ~/phInfo
        ./pathagar-setup.sh
        cd ~/pathagar

There remains to set a pathagar superuser password. Pick a
password ('pi::superuser' for example, make a note of it
so as not to forget,) then proceed with the following:

        cd ~/phInfo
        source penv/bin/activate
        python manage.py createsuperuser
        deactivate

##### Adding Content

Consult the README file in the `pathagar` directory/repository for
instructions how to load books (and other library content) once
the pathagar server is running.

##### Before Final Deployment

Once everything is working as it should, before putting your
server into service, edit `/home/pi/pathagar/localsettings.py`.
Change `DEBUG = True` to `DEBUG = False`.
You will probably also want to change the value of 
`TIME_ZONE = 'America/Los_Angeles'`
Look at `/usr/share/zoneinfo` on any Linux system for guidance as
to how to specify your particular zone.

### Add Another Static Content Site

Still need to document this.


<div></div>
### FOOTNOTES

<a name="1sdcard">1</a>.
    
    128GB cards are available and are said to work
    in the most recent (v3) models of the `Raspberry
    Pi` but we've not tested this.

<a name="2arpscan">2</a>.

    There are various methods of discovering the IP address of the
    `Raspberry Pi`.  Use of the `arp-scan` utility is one.  The
    included `find_pi.py` script uses `arp-scan` and might be useful
    to you but it will have to be customized to suit your own network
    and the devices you own.  Edit `find_pi.py` and read its docstring
    for further details.

<a name="3username">3</a>.

    The scripts assume user name `pi` and that you are cloning the
    `phInfo` repository and `pathagar` into `/home/pi`.  If you decide
    on a different user or use of a different installation directory,
    the scripts will have to be modified accordingly

<a name="4reponame">4</a>.

    The repository name may change in which case all references to
    `phInfo` will need to be changed.

