import math
from dipole import Dipole


class TestHalfWaveDipole:

    def test_half_wave_dipole_100mhz(self, dipole_args):
        d = Dipole(dipole_args)
        length = d.half_wave_dipole(100e6)
        assert math.isclose(length, 1.5, rel_tol=1e-9)

    def test_half_wave_dipole_scaling(self, dipole_args):
        d = Dipole(dipole_args)
        l1 = d.half_wave_dipole(100e6)
        l2 = d.half_wave_dipole(200e6)
        assert math.isclose(l1 / l2, 2.0, rel_tol=1e-9)

    def test_calculator_variable_return(self, dipole_args):
        d = Dipole(dipole_args)
        result = d.half_wave_dipole_calculator()
        assert result is not None
        assert math.isclose(result, 1.5, rel_tol=1e-9)
