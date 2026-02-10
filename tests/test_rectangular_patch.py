import math
import pytest
from rectangular_patch import RectangularPatch


class TestPatchWidth:

    def test_patch_width_at_2_4ghz(self, patch_args):
        rp = RectangularPatch(patch_args)
        W = rp.patch_width(2.4e9, 4.4)
        expected = (3e8 / (2 * 2.4e9)) * math.sqrt(2 / (4.4 + 1))
        assert math.isclose(W, expected, rel_tol=1e-9)


class TestEffectivePermittivity:

    def test_ereff_bounds(self, patch_args):
        rp = RectangularPatch(patch_args)
        W = rp.patch_width(2.4e9, 4.4)
        ereff = rp.effective_relative_permittivity(2.4e9, 4.4, 1.6e-3, W)
        assert 1.0 < ereff < 4.4


class TestDeltaLength:

    def test_delta_length_positive(self, patch_args):
        rp = RectangularPatch(patch_args)
        W = rp.patch_width(2.4e9, 4.4)
        ereff = rp.effective_relative_permittivity(2.4e9, 4.4, 1.6e-3, W)
        dL = rp.delta_length(1.6e-3, ereff, W)
        assert dL > 0


class TestEffectiveLength:

    def test_effective_length_positive(self, patch_args):
        rp = RectangularPatch(patch_args)
        W = rp.patch_width(2.4e9, 4.4)
        ereff = rp.effective_relative_permittivity(2.4e9, 4.4, 1.6e-3, W)
        Leff = rp.effective_length(2.4e9, ereff)
        assert Leff > 0


class TestFeedPoint:

    def test_y0_is_half_width(self, patch_args):
        rp = RectangularPatch(patch_args)
        W = 0.038
        y0 = rp.y0_calculation(W)
        assert math.isclose(y0, W / 2, rel_tol=1e-9)

    def test_x0_invalid_impedance(self, patch_args):
        rp = RectangularPatch(patch_args)
        with pytest.raises(ValueError, match="exceeds the edge impedance"):
            rp.x0_calculation(L=0.01, W=0.05, er=4.4, Z0=9999)


class TestStriplineWidth:

    def test_ws_positive(self, patch_args):
        rp = RectangularPatch(patch_args)
        ws = rp.ws_calculation(1.6e-3, 50, 4.4)
        assert ws > 0


class TestPatchCalculator:

    def test_microstrip_calculator(self, patch_args):
        rp = RectangularPatch(patch_args)
        result = rp.microstrip_patch_calculator()
        assert result is not None

    def test_probe_calculator(self, patch_probe_args):
        rp = RectangularPatch(patch_probe_args)
        result = rp.microstrip_patch_calculator()
        assert result is not None
