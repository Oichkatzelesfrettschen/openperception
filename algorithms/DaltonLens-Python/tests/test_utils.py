"""Tests for daltonlens/utils.py - utility functions."""
import numpy as np
import pytest

from daltonlens import utils


class TestNormalized:
    def test_unit_vector_unchanged(self):
        p = np.array([1.0, 0.0, 0.0])
        result = utils.normalized(p)
        np.testing.assert_allclose(result, p, atol=1e-7)

    def test_result_has_unit_length(self):
        p = np.array([3.0, 4.0])
        result = utils.normalized(p)
        np.testing.assert_allclose(np.linalg.norm(result), 1.0, atol=1e-7)

    def test_arbitrary_vector(self):
        p = np.array([1.0, 2.0, 3.0])
        result = utils.normalized(p)
        np.testing.assert_allclose(np.linalg.norm(result), 1.0, atol=1e-7)


class TestArrayToCDecl:
    def test_1d_array(self):
        a = np.array([1.0, 2.0, 3.0])
        result = utils.array_to_C_decl("test_var", a)
        assert "static float test_var[] = {" in result
        assert "1.00000" in result
        assert result.endswith("};")

    def test_2d_array(self):
        a = np.array([[1.0, 0.0], [0.0, 1.0]])
        result = utils.array_to_C_decl("mat", a)
        assert "static float mat[] = {" in result
        # Should have two rows separated by comma-newline
        assert ",\n" in result

    def test_varname_in_output(self):
        a = np.array([0.5])
        result = utils.array_to_C_decl("my_array", a)
        assert "my_array" in result

    def test_float_precision(self):
        a = np.array([0.123456789])
        result = utils.array_to_C_decl("x", a)
        # Should have 5 decimal places
        assert "0.12346" in result
