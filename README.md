# DRV8830Pico
## Library to control the DRV8830 from a Raspberry Pico

This is a simple library that should allow you to control a DRV8830 driver from a Raspberry Pico. 
An example of a product that can be controlled using this library is this:
https://shop.pimoroni.com/products/drv8830-dc-motor-driver-breakout

## Features

- Simple to use
- Features all I2C commands supported by the DRV8830 - drive forward, backwards, brake, coast and fault reading, with adjustible voltage
- Only requires the basic machine.i2c import, no further dependencies
- Example file included
- Optional debug print inside the library

## Installation

Put it in the lib/drv8830pico/ folder in your project root, import with:

```python
import drv8830pico
```

## Usage

Please see the examples/example.py file for sample usage.

## License

MIT
