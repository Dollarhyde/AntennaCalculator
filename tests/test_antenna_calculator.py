import math
from antenna_calculator import AntennaCalculator


class TestAntennaCalculatorCLI:

    def test_half_wave_dipole_cli(self):
        ac = AntennaCalculator(
            ["half_wave_dipole", "-f", "100e6", "--variable_return"]
        )
        ac.main(ac.getArgs())
        result = ac.getCalcedParams()
        assert result is not None
        assert math.isclose(result, 1.5, rel_tol=1e-9)

    def test_quarter_wave_monopole_cli(self):
        ac = AntennaCalculator(
            ["quarter_wave_monopole", "-f", "100e6", "--variable_return"]
        )
        ac.main(ac.getArgs())
        result = ac.getCalcedParams()
        assert result is not None
        assert math.isclose(result, 0.75, rel_tol=1e-9)

    def test_rectangular_patch_cli(self):
        ac = AntennaCalculator(
            [
                "rectangular_patch",
                "-f", "2.4e9",
                "-er", "4.4",
                "-h", "1.6e-3",
                "--variable_return",
            ]
        )
        ac.main(ac.getArgs())
        result = ac.getCalcedParams()
        assert result is not None

    def test_rectangular_patch_probe_cli(self):
        ac = AntennaCalculator(
            [
                "rectangular_patch",
                "-f", "2.4e9",
                "-er", "4.4",
                "-h", "1.6e-3",
                "--type", "probe",
                "--variable_return",
            ]
        )
        ac.main(ac.getArgs())
        result = ac.getCalcedParams()
        assert result is not None

    def test_dipole_unit_option(self):
        ac = AntennaCalculator(
            ["half_wave_dipole", "-f", "433e6", "-u", "centimeter", "--variable_return"]
        )
        ac.main(ac.getArgs())
        result = ac.getCalcedParams()
        assert result is not None

    def test_monopole_unit_option(self):
        ac = AntennaCalculator(
            [
                "quarter_wave_monopole",
                "-f", "915e6",
                "-u", "millimeter",
                "--variable_return",
            ]
        )
        ac.main(ac.getArgs())
        result = ac.getCalcedParams()
        assert result is not None
