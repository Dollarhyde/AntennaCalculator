#! /usr/bin/python3

import sys
import os
import io
import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from antenna_calculator import AntennaCalculator


def build_rectangular_patch_view(page: ft.Page):

    frequency_field = ft.TextField(
        label="Frequency",
        hint_text="e.g. 2.4",
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.ON_SURFACE,
    )
    frequency_unit = ft.Dropdown(
        label="Unit",
        width=100,
        options=[
            ft.dropdown.Option("GHz"),
            ft.dropdown.Option("MHz"),
            ft.dropdown.Option("kHz"),
            ft.dropdown.Option("Hz"),
        ],
        value="GHz",
        border_color=ft.Colors.ON_SURFACE,
    )
    permittivity_field = ft.TextField(
        label="Relative Permittivity (εr)",
        hint_text="e.g. 4.4",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.ON_SURFACE,
    )
    height_field = ft.TextField(
        label="Substrate Height",
        hint_text="e.g. 1.6",
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.ON_SURFACE,
    )
    height_unit = ft.Dropdown(
        label="Unit",
        width=100,
        options=[
            ft.dropdown.Option("mm"),
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("m"),
            ft.dropdown.Option("mil"),
            ft.dropdown.Option("inch"),
        ],
        value="mm",
        border_color=ft.Colors.ON_SURFACE,
    )
    impedance_field = ft.TextField(
        label="Impedance (Ω)",
        hint_text="default: 50",
        value="50",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.ON_SURFACE,
    )
    feed_type_dropdown = ft.Dropdown(
        label="Feed Type",
        width=300,
        options=[
            ft.dropdown.Option("microstrip"),
            ft.dropdown.Option("probe"),
        ],
        value="microstrip",
        border_color=ft.Colors.ON_SURFACE,
    )
    unit_dropdown = ft.Dropdown(
        label="Output Unit",
        width=300,
        options=[
            ft.dropdown.Option("meter"),
            ft.dropdown.Option("centimeter"),
            ft.dropdown.Option("millimeter"),
            ft.dropdown.Option("inch"),
        ],
        value="millimeter",
        border_color=ft.Colors.ON_SURFACE,
    )
    verbose_switch = ft.Switch(label="Verbose Output", value=False)

    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Parameter")),
            ft.DataColumn(ft.Text("Value")),
        ],
        rows=[],
        visible=False,
    )
    console_output = ft.TextField(
        label="Console Output",
        multiline=True,
        min_lines=6,
        max_lines=15,
        read_only=True,
        visible=False,
        expand=True,
        text_size=12,
        text_style=ft.TextStyle(font_family="Courier New"),
        border_color=ft.Colors.ON_SURFACE,
    )
    status_text = ft.Text("", color=ft.Colors.RED)

    dxf_unit_dropdown = ft.Dropdown(
        label="DXF Unit",
        width=200,
        options=[
            ft.dropdown.Option("meter"),
            ft.dropdown.Option("centimeter"),
            ft.dropdown.Option("millimeter"),
            ft.dropdown.Option("inch"),
        ],
        border_color=ft.Colors.ON_SURFACE,
    )

    png_picker = ft.FilePicker(
        on_result=lambda e: _on_png_picked(e),
    )
    dxf_picker = ft.FilePicker(
        on_result=lambda e: _on_dxf_picked(e),
    )
    gerber_picker = ft.FilePicker(
        on_result=lambda e: _on_gerber_picked(e),
    )
    page.overlay.extend([png_picker, dxf_picker, gerber_picker])

    calc_state = {
        "W": None, "L": None, "x0": None, "y0": None, "ws": None,
        "calculated": False,
    }

    def _validate_inputs():
        errors = []
        for field, name in [
            (frequency_field, "Frequency"),
            (permittivity_field, "Relative Permittivity"),
            (height_field, "Substrate Height"),
        ]:
            if not field.value or field.value.strip() == "":
                errors.append(f"{name} is required.")
                field.error_text = "Required"
            else:
                try:
                    float(field.value)
                    field.error_text = None
                except ValueError:
                    errors.append(f"{name} must be a number.")
                    field.error_text = "Must be a number"

        if impedance_field.value and impedance_field.value.strip() != "":
            try:
                float(impedance_field.value)
                impedance_field.error_text = None
            except ValueError:
                errors.append("Impedance must be a number.")
                impedance_field.error_text = "Must be a number"

        if errors:
            status_text.value = "; ".join(errors)
            status_text.color = ft.Colors.RED
            page.update()
            return False
        return True

    def _freq_to_hz(value, unit):
        multipliers = {"GHz": 1e9, "MHz": 1e6, "kHz": 1e3, "Hz": 1}
        return float(value) * multipliers[unit]

    def _height_to_meters(value, unit):
        multipliers = {"mm": 1e-3, "cm": 1e-2, "m": 1, "mil": 2.54e-5, "inch": 0.0254}
        return float(value) * multipliers[unit]

    def _build_args(variable_return=True, dxf_file=None, png_file=None, gerber_file=None):
        freq_hz = _freq_to_hz(frequency_field.value.strip(), frequency_unit.value)
        height_m = _height_to_meters(height_field.value.strip(), height_unit.value)
        args = [
            "rectangular_patch",
            "-f", str(freq_hz),
            "-er", permittivity_field.value.strip(),
            "-h", str(height_m),
            "--type", feed_type_dropdown.value,
        ]
        if impedance_field.value and impedance_field.value.strip():
            args.extend(["-Z0", impedance_field.value.strip()])
        if unit_dropdown.value:
            args.extend(["-u", unit_dropdown.value])
        if verbose_switch.value:
            args.append("--verbose")
        if variable_return:
            args.append("--variable_return")
        if dxf_file:
            args.extend(["--dxfoutput", dxf_file])
            if dxf_unit_dropdown.value:
                args.extend(["-du", dxf_unit_dropdown.value])
        if png_file:
            args.extend(["--pngoutput", png_file])
        if gerber_file:
            args.extend(["--gerberoutput", gerber_file])
            if dxf_unit_dropdown.value:
                args.extend(["-du", dxf_unit_dropdown.value])
        return args

    def on_calculate(e):
        if not _validate_inputs():
            return

        try:
            captured = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured

            args_print = _build_args(variable_return=False)
            shell_print = AntennaCalculator(a=args_print)
            shell_print.main(shell_print.getArgs())

            sys.stdout = old_stdout
            printed_output = captured.getvalue()

            args_return = _build_args(variable_return=True)
            shell_return = AntennaCalculator(a=args_return)
            shell_return.main(shell_return.getArgs())
            params = shell_return.getCalcedParams()

            if params is None:
                status_text.value = "Calculation returned no results."
                status_text.color = ft.Colors.RED
                results_table.visible = False
                page.update()
                return

            if feed_type_dropdown.value == "microstrip" and len(params) == 5:
                W, L, x0, y0, ws = params
                calc_state.update({"W": W, "L": L, "x0": x0, "y0": y0, "ws": ws, "calculated": True})
            elif feed_type_dropdown.value == "probe" and len(params) == 4:
                W, L, x0, y0 = params
                calc_state.update({"W": W, "L": L, "x0": x0, "y0": y0, "ws": None, "calculated": True})
            else:
                W, L, x0, y0 = params[:4]
                ws = params[4] if len(params) > 4 else None
                calc_state.update({"W": W, "L": L, "x0": x0, "y0": y0, "ws": ws, "calculated": True})

            results_table.rows.clear()
            for line in printed_output.strip().split("\n"):
                if line.startswith("[*]"):
                    parts = line[3:].strip().split("=", 1)
                    if len(parts) == 2:
                        results_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(parts[0].strip())),
                                ft.DataCell(ft.Text(parts[1].strip())),
                            ])
                        )
            results_table.visible = True

            if printed_output.strip():
                console_output.value = printed_output.strip()
                console_output.visible = True
            else:
                console_output.visible = False

            status_text.value = "Calculation complete."
            status_text.color = ft.Colors.GREEN_400

        except Exception as ex:
            sys.stdout = old_stdout if 'old_stdout' in dir() else sys.__stdout__
            status_text.value = f"Error: {str(ex)}"
            status_text.color = ft.Colors.RED
            results_table.visible = False
            console_output.visible = False

        page.update()

    def _run_export(dxf_file=None, png_file=None, gerber_file=None):
        if not calc_state["calculated"]:
            status_text.value = "Run Calculate first before exporting."
            status_text.color = ft.Colors.RED
            page.update()
            return
        if not _validate_inputs():
            return

        try:
            captured = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured

            args = _build_args(
                variable_return=False,
                dxf_file=dxf_file,
                png_file=png_file,
                gerber_file=gerber_file,
            )
            shell = AntennaCalculator(a=args)
            shell.main(shell.getArgs())

            sys.stdout = old_stdout
            printed = captured.getvalue()

            current = console_output.value or ""
            console_output.value = current + "\n" + printed.strip() if current else printed.strip()
            console_output.visible = True

            export_type = "PNG" if png_file else "DXF" if dxf_file else "Gerber"
            status_text.value = f"{export_type} export complete."
            status_text.color = ft.Colors.GREEN_400

        except Exception as ex:
            sys.stdout = old_stdout if 'old_stdout' in dir() else sys.__stdout__
            status_text.value = f"Export error: {str(ex)}"
            status_text.color = ft.Colors.RED

        page.update()

    def _on_png_picked(e: ft.FilePickerResultEvent):
        if e.path:
            path = e.path if e.path.lower().endswith(".png") else e.path + ".png"
            _run_export(png_file=path)

    def _on_dxf_picked(e: ft.FilePickerResultEvent):
        if e.path:
            path = e.path if e.path.lower().endswith(".dxf") else e.path + ".dxf"
            _run_export(dxf_file=path)

    def _on_gerber_picked(e: ft.FilePickerResultEvent):
        if e.path:
            _run_export(gerber_file=e.path)

    def on_export_png(e):
        if not calc_state["calculated"]:
            status_text.value = "Run Calculate first before exporting."
            status_text.color = ft.Colors.RED
            page.update()
            return
        png_picker.save_file(
            dialog_title="Save PNG File",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["png"],
            file_name="antenna.png",
        )

    def on_export_dxf(e):
        if not calc_state["calculated"]:
            status_text.value = "Run Calculate first before exporting."
            status_text.color = ft.Colors.RED
            page.update()
            return
        dxf_picker.save_file(
            dialog_title="Save DXF File",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["dxf"],
            file_name="antenna.dxf",
        )

    def on_export_gerber(e):
        if not calc_state["calculated"]:
            status_text.value = "Run Calculate first before exporting."
            status_text.color = ft.Colors.RED
            page.update()
            return
        gerber_picker.save_file(
            dialog_title="Save Gerber Files (base name)",
            file_name="antenna_gerber",
        )

    calculate_btn = ft.ElevatedButton(
        "Calculate",
        icon=ft.Icons.CALCULATE,
        on_click=on_calculate,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.ON_PRIMARY,
        ),
    )

    export_row = ft.Row(
        controls=[
            ft.OutlinedButton("Export PNG", icon=ft.Icons.IMAGE, on_click=on_export_png),
            ft.OutlinedButton("Export DXF", icon=ft.Icons.ARCHITECTURE, on_click=on_export_dxf),
            ft.OutlinedButton("Export Gerber", icon=ft.Icons.LAYERS, on_click=on_export_gerber),
            dxf_unit_dropdown,
        ],
        spacing=10,
        wrap=True,
    )

    view = ft.Column(
        controls=[
            ft.Text("Rectangular Patch Antenna", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.ResponsiveRow(
                controls=[
                    ft.Column(col={"sm": 12, "md": 6}, controls=[
                        ft.Row([frequency_field, frequency_unit], spacing=5),
                        permittivity_field,
                        ft.Row([height_field, height_unit], spacing=5),
                    ]),
                    ft.Column(col={"sm": 12, "md": 6}, controls=[
                        impedance_field,
                        feed_type_dropdown,
                        unit_dropdown,
                    ]),
                ],
            ),
            verbose_switch,
            ft.Row(controls=[calculate_btn], spacing=10),
            status_text,
            ft.Divider(),
            ft.Text("Results", size=18, weight=ft.FontWeight.W_500),
            results_table,
            ft.Divider(),
            ft.Text("Export", size=18, weight=ft.FontWeight.W_500),
            export_row,
            ft.Divider(),
            console_output,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return view
