import math
from dipole import Dipole
from monopole import Monopole


class TestQuarterWaveMonopole:

    def test_quarter_wave_monopole_100mhz(self, monopole_args):
        m = Monopole(monopole_args)
        length = m.quarter_wave_monopole(100e6)
        assert math.isclose(length, 0.75, rel_tol=1e-9)

    def test_monopole_dipole_ratio(self, monopole_args):
        freq = 500e6
        d = Dipole(monopole_args)
        m = Monopole(monopole_args)
        dipole_len = d.half_wave_dipole(freq)
        monopole_len = m.quarter_wave_monopole(freq)
        assert math.isclose(monopole_len, dipole_len / 2, rel_tol=1e-9)

    def test_calculator_variable_return(self, monopole_args):
        m = Monopole(monopole_args)
        result = m.quarter_wave_monopole_calculator()
        assert result is not None
        assert math.isclose(result, 0.75, rel_tol=1e-9)
