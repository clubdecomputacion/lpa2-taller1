"""
Pruebas de la clase abstracta Almacenamiento.
"""

import pytest

from models.mueble import Mueble
from models.categorias.almacenamiento import Almacenamiento
from tests.unit.conftest import AlmacenamientoConcreto


class TestAlmacenamientoAbstracto:
    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Almacenamiento("Armario", "Madera", "Café", 100.0, 2, 100)

    def test_hereda_de_mueble(self, almacenamiento):
        assert isinstance(almacenamiento, Mueble)


class TestAlmacenamientoAtributos:
    def test_constructor_asigna_atributos(self, almacenamiento):
        assert almacenamiento.num_compartimentos == 3
        assert almacenamiento.capacidad_litros == 200

    def test_setters_validos(self, almacenamiento):
        almacenamiento.num_compartimentos = 5
        almacenamiento.capacidad_litros = 50.5
        assert almacenamiento.num_compartimentos == 5
        assert almacenamiento.capacidad_litros == 50.5

    @pytest.mark.parametrize("valor", [0, -2])
    def test_compartimentos_invalidos_lanzan_error(self, almacenamiento, valor):
        with pytest.raises(ValueError, match="compartimentos debe ser mayor a 0"):
            almacenamiento.num_compartimentos = valor

    @pytest.mark.parametrize("valor", [0, -10])
    def test_capacidad_invalida_lanza_error(self, almacenamiento, valor):
        with pytest.raises(ValueError, match="capacidad debe ser mayor a 0"):
            almacenamiento.capacidad_litros = valor


class TestFactorAlmacenamiento:
    @pytest.mark.parametrize(
        "compartimentos,litros,esperado",
        [
            (1, 0.0001, 1.0),
            (3, 200, 1.14),
            (5, 100, 1.22),
        ],
    )
    def test_calcular_factor(self, compartimentos, litros, esperado):
        mueble = AlmacenamientoConcreto("A", "Madera", "Café", 100.0, compartimentos, litros)
        assert mueble.calcular_factor_almacenamiento() == pytest.approx(esperado, abs=1e-4)

    def test_info_almacenamiento(self, almacenamiento):
        assert almacenamiento.obtener_info_almacenamiento() == (
            "Compartimentos: 3, Capacidad: 200L"
        )
