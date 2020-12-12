# IKEA Tradfri light control

This is a very quickly made script for turning on IKEA Tradfri lights when entering calls on Webex devices.
It will also turn the lights off after exiting the call. While it's not super secure (allowing anyone on the local network to control it without a token), it does its thing well enough.
It uses `pytradfri` for communicating with an IKEA gateway and `Flask` to serve a REST interface.

