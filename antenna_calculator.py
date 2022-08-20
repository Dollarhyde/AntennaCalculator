import argparse

main_parser = argparse.ArgumentParser(description='Antenna Calculator', add_help=False)
main_parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
main_parser.add_argument('--version', action='version', version='%(prog)s 1.0')

subparsers=main_parser.add_subparsers(help='sub-command help', dest='subparser_name')

rectangular_patch_subparser = subparsers.add_parser('rectangular_patch', add_help=False)
rectangular_patch_subparser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
rectangular_patch_subparser.add_argument('--verbose', action='store_true')
rectangular_patch_subparser.add_argument('--type', type=str, choices=['microstrip', 'probe'], default='microstrip', help='Type of patch')
rectangular_patch_subparser.add_argument('-f', '--frequency', type=float, required=True, help='Frequency in Hz')
rectangular_patch_subparser.add_argument('-er', '--relative_permittivity', type=float, required=True, help='Relative permittivity')
rectangular_patch_subparser.add_argument('-h', '--height', type=float, required=True, help='Substrate height in meters')
rectangular_patch_subparser.add_argument('-u', '--unit', type=str, choices=['meter','centimeter', 'millimeter', 'inch'], required=False, help='Unit of measurement')
rectangular_patch_subparser.add_argument('-du', '--dxfunit', type=str, choices=['meter','centimeter', 'millimeter', 'inch'], required=False, help='DXF Unit of measurement')
rectangular_patch_subparser.add_argument('--dxfoutput', type=str, required=False, default='patch.dxf', help='Name of DXF file')
rectangular_patch_subparser.add_argument('--pngoutput', type=str, required=False, default='patch.png', help='Name of PNG image for printing')
rectangular_patch_subparser.add_argument('--variable_return', action='store_true', required=False, default=False, help='Return Variables instead of printing')

rectangular_patch_export_subparser = subparsers.add_parser('rectangular_patch_export', add_help=False)
rectangular_patch_export_subparser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
rectangular_patch_export_subparser.add_argument('--verbose', action='store_true')
rectangular_patch_export_subparser.add_argument('--type', type=str, choices=['microstrip', 'probe'], default='microstrip', help='Type of patch')
rectangular_patch_export_subparser.add_argument('-W', '--width', type=float, required=True, help='width in meters')
rectangular_patch_export_subparser.add_argument('-L', '--length', type=float, required=True, help='length in meters')
rectangular_patch_export_subparser.add_argument('-x0', type=float, required=True, help='x0 in meters')
rectangular_patch_export_subparser.add_argument('-y0', type=float, required=True, help='y0 in meters')
rectangular_patch_export_subparser.add_argument('-ws', '--strip_width', type=float, required=False, help='width spacing in meters')
rectangular_patch_export_subparser.add_argument('-du', '--dxfunit', type=str, choices=['meter','centimeter', 'millimeter', 'inch'], required=False, help='DXF Unit of measurement')
rectangular_patch_export_subparser.add_argument('--dxfoutput', type=str, required=False, default='patch.dxf', help='Name of DXF file')
rectangular_patch_export_subparser.add_argument('--pngoutput', type=str, required=False, default='patch.png', help='Name of PNG image for printing')

half_wave_dipole_subparser = subparsers.add_parser('half_wave_dipole', add_help=False)
half_wave_dipole_subparser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
half_wave_dipole_subparser.add_argument('--verbose', action='store_true')
half_wave_dipole_subparser.add_argument('-f', '--frequency', type=float, required=True, help='Frequency in Hz')
half_wave_dipole_subparser.add_argument('-u', '--unit', type=str, choices=['meter','centimeter', 'millimeter', 'inch'], required=False, help='Unit of measurement')

quarter_wave_monopole_subparser = subparsers.add_parser('quarter_wave_monopole', add_help=False)
quarter_wave_monopole_subparser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
quarter_wave_monopole_subparser.add_argument('--verbose', action='store_true')
quarter_wave_monopole_subparser.add_argument('-f', '--frequency', type=float, required=True, help='Frequency in Hz')
quarter_wave_monopole_subparser.add_argument('-u', '--unit', type=str, choices=['meter','centimeter', 'millimeter', 'inch'], required=False, help='Unit of measurement')

args = main_parser.parse_args()

def main():
    if args.subparser_name == 'rectangular_patch':
        import rectangular_patch
        rectangular_patch.microstrip_patch_calculator()

    if args.subparser_name == 'rectangular_patch_export':
        import rectangular_patch
        if args.pngoutput:
            rectangular_patch.export_patch_to_png()
        if args.dxfoutput:
            rectangular_patch.export_patch_to_dxf()

    if args.subparser_name == 'half_wave_dipole':
        import dipole
        dipole.half_wave_dipole_calculator()
    
    if args.subparser_name == 'quarter_wave_monopole':
        import monopole
        monopole.quarter_wave_monopole_calculator()

if __name__ ==  "__main__":
    main()
    