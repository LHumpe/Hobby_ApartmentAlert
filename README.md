# ApartmentAlter - Python CLT for Apartment Search Notifications

This repo contains a programm that I used when I was looking for an appartment in Cologne. It ran as an automated
subprocess on my Raspberry Pi shutting off during nights and booting up in the mornings. Whenever there is a new
apartment appearing the agent sends an email to user with the link so that the holder of the apartment can be contacted.
Even though, the code is very basic and probably not the cleanest, this was one of my first projects and laid the path
for many other webscrapers.

This package is no longer maintained, i.e. there might be breaking changes in the structure of the Apartment websites
such that the scraper must be modified by you. It currently works with the following websites:

- https://www.wg-gesucht.de/
- https://www.immobilienscout24.de/
- https://www.immonet.de/

# Installation

Within the same folder as ```setup.py``` run ```pip3 install .``` to install the package. Use flag ```-e``` to install
in development mode.

# Basic Usage

Go to one of the above URLs and set your search parameters. Copy the resulting URLs and start the agent with the
following CLI command:

```
ApartmentAlert _start_Agent 
        --immoscout_url "<URL from Immobilienscout>" 
        --immonet_url "<URL from Immonet>" 
        --wggesucht_url "<URL from WG-Gesucht>"
        --from_mail "<Mail address from which the emails get sent from>"
        --to_mail  "<Mail address where emails should get sent to>"
        --pw_mail "<Password for sender email address>"
        --smtp_server "<smtpt server for sender email address>"
        --log_path "<absolute path to a logging dir>"
        --stop_time "<HH:MM:SS when the scraper should stop. Useful for RPI usage but not necessary>"
```