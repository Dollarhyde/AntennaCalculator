#! /usr/bin/python3

import sys
import os
import io
import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from antenna_calculator import AntennaCalculator


def build_dipole_view(page: ft.Page):

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
        min_lines=4,
        max_lines=10,
        read_only=True,
        visible=False,
        expand=True,
        text_size=12,
        text_style=ft.TextStyle(font_family="Courier New"),
        border_color=ft.Colors.ON_SURFACE,
    )
    status_text = ft.Text("", color=ft.Colors.RED)

    def _validate_inputs():
        if not frequency_field.value or frequency_field.value.strip() == "":
            frequency_field.error_text = "Required"
            status_text.value = "Frequency is required."
            status_text.color = ft.Colors.RED
            page.update()
            return False
        try:
            float(frequency_field.value)
            frequency_field.error_text = None
        except ValueError:
            frequency_field.error_text = "Must be a number"
            status_text.value = "Frequency must be a number."
            status_text.color = ft.Colors.RED
            page.update()
            return False
        return True

    def on_calculate(e):
        if not _validate_inputs():
            return

        try:
            captured = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured

            freq_hz = str(float(frequency_field.value.strip()) * {"GHz": 1e9, "MHz": 1e6, "kHz": 1e3, "Hz": 1}[frequency_unit.value])
            args = [
                "half_wave_dipole",
                "-f", freq_hz,
            ]
            if unit_dropdown.value:
                args.extend(["-u", unit_dropdown.value])
            if verbose_switch.value:
                args.append("--verbose")

            shell = AntennaCalculator(a=args)
            shell.main(shell.getArgs())

            sys.stdout = old_stdout
            printed_output = captured.getvalue()

            args_return = list(args) + ["--variable_return"]
            shell_return = AntennaCalculator(a=args_return)
            shell_return.main(shell_return.getArgs())
            params = shell_return.getCalcedParams()

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

    calculate_btn = ft.ElevatedButton(
        "Calculate",
        icon=ft.Icons.CALCULATE,
        on_click=on_calculate,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.ON_PRIMARY,
        ),
    )

    view = ft.Column(
        controls=[
            ft.Text("Half-Wave Dipole Antenna", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.ResponsiveRow(
                controls=[
                    ft.Column(col={"sm": 12, "md": 6}, controls=[
                        ft.Row([frequency_field, frequency_unit], spacing=5),
                    ]),
                    ft.Column(col={"sm": 12, "md": 6}, controls=[
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
            console_output,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return view
