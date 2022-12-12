# AntennaCalculator

Open Source Antenna Designer

```
usage: antenna_calculator.py [--help] [--version] {rectangular_patch,half_wave_dipole,quarter_wave_monopole} ...

Antenna Calculator

positional arguments:
  {rectangular_patch,half_wave_dipole,quarter_wave_monopole}
                        sub-command help

optional arguments:
  --help                Show this help message and exit
  --version             show program's version number and exit
```

```
usage: antenna_calculator.py rectangular_patch [--help] [--verbose] [--type {microstrip,probe}] -f FREQUENCY -er RELATIVE_PERMITTIVITY -h HEIGHT
                                               [-u {meter,centimeter,millimeter,inch}] [-du {meter,centimeter,millimeter,inch}] [--dxfoutput DXFOUTPUT]
                                               [--pngoutput PNGOUTPUT]

optional arguments:
  --help                Show this help message and exit
  --verbose
  --type {microstrip,probe}
                        Type of patch
  -f FREQUENCY, --frequency FREQUENCY
                        Frequency in Hz
  -er RELATIVE_PERMITTIVITY, --relative_permittivity RELATIVE_PERMITTIVITY
                        Relative permittivity
  -h HEIGHT, --height HEIGHT
                        Substrate height in meters
  -u {meter,centimeter,millimeter,inch}, --unit {meter,centimeter,millimeter,inch}
                        Unit of measurement
  -du {meter,centimeter,millimeter,inch}, --dxfunit {meter,centimeter,millimeter,inch}
                        DXF Unit of measurement
  --dxfoutput DXFOUTPUT
                        Name of DXF file
  --pngoutput PNGOUTPUT
                        Name of PNG image for printing
```
```
usage: antenna_calculator.py half_wave_dipole [--help] [--verbose] -f FREQUENCY [-u {meter,centimeter,millimeter,inch}]

optional arguments:
  --help                Show this help message and exit
  --verbose
  -f FREQUENCY, --frequency FREQUENCY
                        Frequency in Hz
  -u {meter,centimeter,millimeter,inch}, --unit {meter,centimeter,millimeter,inch}
                        Unit of measurement
```
```
usage: antenna_calculator.py quarter_wave_monopole [--help] [--verbose] -f FREQUENCY [-u {meter,centimeter,millimeter,inch}]

optional arguments:
  --help                Show this help message and exit
  --verbose
  -f FREQUENCY, --frequency FREQUENCY
                        Frequency in Hz
  -u {meter,centimeter,millimeter,inch}, --unit {meter,centimeter,millimeter,inch}
                        Unit of measurement
```

## Rectangular Patch Example

```
python3 antenna_calculator.py rectangular_patch -f 2.4e9 -er 4.4 -h 1.6e-3
[*] W = 38.04 millimeter
[*] L = 29.44 millimeter
[*] Ws = 3.06 millimeter
[*] y0 = 19.02 millimeter
[*] x0 = 11.32 millimeter
```

## PNG output using `--pngoutput`

![image](https://user-images.githubusercontent.com/18094862/184426961-36c21cbd-9cff-4c4b-a275-a81e187ce86c.png)

## DXF output using `--dxfoutput`

![image](https://user-images.githubusercontent.com/18094862/184427196-34eb8369-11e8-48cb-9426-3251ef8c7e84.png)

## Gerber output using `--gerberoutput`
![image](https://user-images.githubusercontent.com/18094862/187831470-c8cb4801-b0c9-44e2-acc7-454ad2d03f37.png)

# DEFCON Presentation
[![DEFCON Presentation](https://i.ytimg.com/vi/7mciNPmT1KE/hqdefault.jpg)](https://www.youtube.com/watch?v=7mciNPmT1KE "DEF CON 30 RF Village - Erwin Karincic - Have a SDR? - Design and make your own antennas")
## PDF presentation
[PDF link](https://github.com/Dollarhyde/AntennaCalculator/blob/main/Have%20a%20Software%20Defined%20Radio%20-%20Design%20and%20make%20your%20own%20antennas.pdf)
