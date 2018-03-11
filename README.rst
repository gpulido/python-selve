Python control of selve devices through USB-RF Gateway
======================================================
A simple Python API for controlling RF Blinds / shutters / awning from selve using a USB-RF Gateway.
At present, only Iveo devices are supported.

The complete protocol specification can be found at `selve <https://www.selve.de/de/service/software-updates/service-entwicklungstool-commeo-usb-rf-gateway/>`_

Example of use
--------------

Create a new instance of the gateway:

```python
gat = Gateway(portname)
```

portname is the name of the serial port where the usb rf gateway is listed on the os. Please refer to the serial library documentation.

By default the gateway will discover all Iveo devices already registered onto the gateway.

To access them:

```python
gat.devices()
```

Will return a list of IveoDevices()

Each IveoDevice can be controlled by using the already defined commands: stop() moveUp() moveToIntermediatePosition1() and moveToIntermediatePosition2()

The library also allows to send directly commands to the gateway without the need of using the IveoDevice abstraction just create the command and execute using the gateway:

```python
command = IveoCommandGetIds()
command.execute(gat)
```

Once executed the response is stored in the command instance for later user or just to discard.






