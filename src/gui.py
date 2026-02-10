#! /usr/bin/python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from views.rectangular_patch_view import build_rectangular_patch_view
from views.dipole_view import build_dipole_view
from views.monopole_view import build_monopole_view


def main(page: ft.Page):
    page.title = "Antenna Calculator"
    page.window.width = 960
    page.window.height = 720
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    patch_view = build_rectangular_patch_view(page)
    dipole_view = build_dipole_view(page)
    monopole_view = build_monopole_view(page)

    # Container that holds the active view
    content_area = ft.Container(
        content=patch_view,
        expand=True,
        padding=20,
    )

    def on_nav_change(e):
        index = e.control.selected_index
        if index == 0:
            content_area.content = patch_view
        elif index == 1:
            content_area.content = dipole_view
        elif index == 2:
            content_area.content = monopole_view
        page.update()

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.RECTANGLE_OUTLINED,
                selected_icon=ft.Icons.RECTANGLE,
                label="Rect. Patch",
            ),
            ft.NavigationRailDestination(
                icon=ft.CupertinoIcons.DOT_RADIOWAVES_LEFT_RIGHT,
                selected_icon=ft.CupertinoIcons.DOT_RADIOWAVES_LEFT_RIGHT,
                label="Dipole",
            ),
            ft.NavigationRailDestination(
                icon=ft.CupertinoIcons.DOT_RADIOWAVES_RIGHT,
                selected_icon=ft.CupertinoIcons.DOT_RADIOWAVES_RIGHT,
                label="Monopole",
            ),
        ],
        on_change=on_nav_change,
    )

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.CupertinoIcons.ANTENNA_RADIOWAVES_LEFT_RIGHT),
        leading_width=40,
        title=ft.Text("Antenna Calculator", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.PRIMARY,
        color=ft.Colors.ON_PRIMARY,
        actions=[
            ft.IconButton(
                ft.Icons.BRIGHTNESS_6,
                tooltip="Toggle Theme",
                icon_color=ft.Colors.ON_PRIMARY,
                on_click=lambda e: _toggle_theme(page),
            ),
        ],
    )

    def _toggle_theme(page):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    page.add(
        ft.Row(
            controls=[
                nav_rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
