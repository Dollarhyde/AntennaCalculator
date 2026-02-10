from types import SimpleNamespace

import pytest


@pytest.fixture
def dipole_args():
    return SimpleNamespace(
        frequency=100e6,
        unit=None,
        verbose=False,
        variable_return=True,
    )


@pytest.fixture
def monopole_args():
    return SimpleNamespace(
        frequency=100e6,
        unit=None,
        verbose=False,
        variable_return=True,
    )


@pytest.fixture
def patch_args():
    return SimpleNamespace(
        frequency=2.4e9,
        relative_permittivity=4.4,
        height=1.6e-3,
        impedance=50,
        type="microstrip",
        unit=None,
        dxfunit=None,
        verbose=False,
        variable_return=True,
        pngoutput=None,
        dxfoutput=None,
        gerberoutput=None,
    )


@pytest.fixture
def patch_probe_args():
    return SimpleNamespace(
        frequency=2.4e9,
        relative_permittivity=4.4,
        height=1.6e-3,
        impedance=50,
        type="probe",
        unit=None,
        dxfunit=None,
        verbose=False,
        variable_return=True,
        pngoutput=None,
        dxfoutput=None,
        gerberoutput=None,
    )
