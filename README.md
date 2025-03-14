# AntennaCalculator

Open Source Antenna Designer. 

The calculator features the following topologies:
* Rectangular patch antenna, probe and microstrip versions
* Quarter Wave Monopole
* Half Wave Dipole

Supported exports:
* Rectangular patch: top layer PNG, top layer DXF, gerber files


The analytical models for the three topologies are from [1]. The calculated designs have been verified in simulation with Ansys HFSS and experimentation. 

## Table of Contents
* [Requirements](#requirements)
* [Usage](#usage)
    * [Rectangular Patch Usage](#rectangular-patch-usage)
    * [Half Wave Dipole Usage](#half-wave-dipole-usage)
    * [Quarter Wave Monopole Usage](#quarter-wave-monopole-usage)
* [Examples](#example-implementations)
    * [Rectangular Patch](#rectangular-patch)
      * [PNG output using `--pngoutput`](#png-output-using---pngoutput)
      * [DXF output using `--dxfoutput`](#dxf-output-using---dxfoutput)
      * [Gerber output using `--gerberoutput`](#gerber-output-using---gerberoutput)
* [References](#references)
* [Publications and Presentations](#publications-and-presentations)
    * [Papers](#papers)
    * [DEFCON 30 Presentation](#defcon-30-presentation)
      * [Presentation Recording](#presentation-recording)
      * [PDF Presentation](#pdf-presentation)

## Requirements

This project requires numpy, pcb-tools-extension, ezdxf, pint, pillow. 


The AntennaCalculator has been tested on Python 3.9, 3.11, and 3.12. 


Use 'pip install -r requirements.txt' to install the following dependencies:

```python
ezdxf~=0.18
numpy~=1.23.2
pcb-tools~=0.1.6
pcb-tools-extension~=0.9.3
Pillow~=9.5.0
Pint~=0.19.2
```



Or install manually with:
```python
pip install numpy, pcb-tools-extension, ezdxf, pint, pillow

```


## Usage

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

### Rectangular Patch Usage
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

### Half Wave Dipole Usage
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

### Quarter Wave Monopole Usage
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


## Examples

### Rectangular Patch

#### Calculating and Returning Variables


**Standard variable print out:**
```
python antenna_calculator.py rectangular_patch -f 2.4e9 -er 4.4 -h 1.6e-3


[*] W = 38.04 millimeter
[*] L = 29.44 millimeter
[*] x0 = 11.32 millimeter
[*] y0 = 19.02 millimeter
[*] Ws = 3.06 millimeter

```

**Full variable print out:**
```
python antenna_calculator.py rectangular_patch -f 2.4e9 -er 4.4 -h 1.6e-3 --verbose


[*] W = 38.04 millimeter
[*] Ereff = 4.09
[*] dL = 738.82 micrometer
[*] Leff = 30.92 millimeter
[*] Zin_0 = 396.6828700137873
[*] Zin_x0 = 50
[*] x0 = 0.01131973828663886
[*] x0 = 11.32 millimeter
[*] y0 = 0.01901814435781827
[*] y0 = 19.02 millimeter
[*] A = 1.529861949318471
[*] A Ws/d = 1.9118593643297774
[*] A is valid
[*] Ws = 3.06 millimeter
```

**Return variables, no printout:**
```
python antenna_calculator.py rectangular_patch -f 2.4e9 -er 4.4 -h 1.6e-3 --variable_return
```


#### PNG output using `--pngoutput`

```
python antenna_calculator.py rectangular_patch -f 2.4e9 -er 4.4 -h 1.6e-3 --pngoutput myPNG.PNG 


[*] W = 38.04 millimeter
[*] L = 29.44 millimeter
[*] x0 = 11.32 millimeter
[*] y0 = 19.02 millimeter
[*] Ws = 3.06 millimeter
[*] Image saved: myPNG.PNG

```



![image](https://user-images.githubusercontent.com/18094862/184426961-36c21cbd-9cff-4c4b-a275-a81e187ce86c.png)

#### DXF output using `--dxfoutput`

```
python antenna_calculator.py rectangular_patch -f 2.4e9 -er 4.4 -h 1.6e-3 --dxfoutput myDXF.dxf


[*] W = 38.04 millimeter
[*] L = 29.44 millimeter
[*] x0 = 11.32 millimeter
[*] y0 = 19.02 millimeter
[*] Ws = 3.06 millimeter
[*] DXF file generated: myDXF.dxf

```



![image](https://user-images.githubusercontent.com/18094862/184427196-34eb8369-11e8-48cb-9426-3251ef8c7e84.png)

#### Gerber output using `--gerberoutput`

```
python antenna_calculator.py rectangular_patch -f 2.4e9 -er 4.4 -h 1.6e-3 --gerberoutput myGerberFiles


[*] W = 38.04 millimeter
[*] L = 29.44 millimeter
[*] x0 = 11.32 millimeter
[*] y0 = 19.02 millimeter
[*] Ws = 3.06 millimeter
[*] DXF file generated: myGerberFiles
[*] Top Layer DXF file generated: myGerberFiles_top.dxf
[*] Substrate DXF file generated: myGerberFiles_substrate.dxf
[*] Top layer gerber file generated: myGerberFiles_top.gtl
[*] Substrate gerber file generated: myGerberFiles_substrate.gml

```



![image](https://user-images.githubusercontent.com/18094862/187831470-c8cb4801-b0c9-44e2-acc7-454ad2d03f37.png)



## References

[1]: C. A. Balanis, Antenna Theory: Analysis and Design. Hoboken, New Jersey Wiley, 2016.


## Publications and Presentations
### Papers

* E. Karincic, E. Topsakal, and L. Linkous.  "Patch Antenna Calculations and Fabrication Made Simple for Cyber Security Research,"  2023 ASEE Annual Conference & Exposition, Baltimore , Maryland, 2023, June.  ASEE Conferences, 2023. [Online:] https://peer.asee.org/43974 

* L. Linkous, E. Karincic, J. Lundquist and E. Topsakal, "Automated Antenna Calculation, Design and Tuning Tool for HFSS," 2023 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), Boulder, CO, USA, 2023, pp. 229-230, doi: 10.23919/USNC-URSINRSM57470.2023.10043119.

* L. Linkous, J. Lundquist and E. Topsakal, "AntennaCAT: Automated Antenna Design and Tuning Tool," 2023 IEEE USNC-URSI Radio Science Meeting (Joint with AP-S Symposium), Portland, OR, USA, 2023, pp. 89-90, doi: 10.23919/USNC-URSI54200.2023.10289238.


### DEFCON 30 Presentation
#### Presentation Recording
[![DEFCON Presentation](https://i.ytimg.com/vi/7mciNPmT1KE/hqdefault.jpg)](https://www.youtube.com/watch?v=7mciNPmT1KE "DEF CON 30 RF Village - Erwin Karincic - Have a SDR? - Design and make your own antennas")

#### PDF Presentation
["DEF CON 30 RF Village - Erwin Karincic - Have a SDR? - Design and make your own antennas" PDF link](https://github.com/Dollarhyde/AntennaCalculator/blob/main/Have%20a%20Software%20Defined%20Radio%20-%20Design%20and%20make%20your%20own%20antennas.pdf)

