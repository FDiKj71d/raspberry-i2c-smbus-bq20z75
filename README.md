# raspberry-i2c-smbus-bq20z75

A tool for interacting with bq20z75 laptop batteries via Raspberry's I2C pins.
Requires apt-install python3-smbus

When running it prompts for user input:

Select operation:
1. Read pack info.
2. Pack Reset.
3. Unsealing a pack.
4. Move pack to Full Access mode.
5. Clearing a Permanent Failure.
6. Clearing CycleCount.
7. Setting current date.
8. Writing DesignCapacity, QMAX, Update status, Ra_table.
9. Begin the Impedance Track algorithm.
