"""
Pruebas de la clase abstracta Asiento.
"""

import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from tests.unit.conftest import AsientoConcreto


class TestAsientoAbstracto:
    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Asiento("Asiento", "Madera", "Café", 100.0, 1, True)

    def test_hereda_de_mueble(self, asiento):
        assert isinstance(asiento, Mueble)


class TestAsientoAtributos:
    def test_constructor_asigna_atributos(self, asiento):
        assert asiento.capacidad_personas == 3
        assert asiento.tiene_respaldo is True
        assert asiento.material_tapizado == "cuero"

    def test_tapizado_por_defecto_es_none(self):
        asiento = AsientoConcreto("A", "Madera", "Café", 100.0, 1, False)
        assert asiento.material_tapizado is None

    def test_setter_capacidad(self, asiento):
        asiento.capacidad_personas = 5
        assert asiento.capacidad_personas == 5

    @pytest.mark.parametrize("valor", [0, -1])
    def test_setter_capacidad_invalida_lanza_error(self, asiento, valor):
        with pytest.raises(ValueError, match="mayor a 0"):
            asiento.capacidad_personas = valor

    def test_setters_respaldo_y_tapizado(self, asiento):
        asiento.tiene_respaldo = False
        asiento.material_tapizado = "tela"
        assert asiento.tiene_respaldo is False
        assert asiento.material_tapizado == "tela"


class TestFactorComodidad:
    @pytest.mark.parametrize(
        "capacidad,respaldo,tapizado,esperado",
        [
            (1, False, None, 1.0),
            (1, True, None, 1.1),
            (1, False, "cuero", 1.2),
            (1, False, "CUERO", 1.2),
            (1, False, "tela", 1.1),
            (1, False, "lino", 1.0),
            (3, True, "cuero", 1.4),
        ],
    )
    def test_calcular_factor_comodidad(self, capacidad, respaldo, tapizado, esperado):
        asiento = AsientoConcreto("A", "Madera", "Café", 100.0, capacidad, respaldo, tapizado)
        assert asiento.calcular_factor_comodidad() == pytest.approx(esperado)


class TestInfoAsiento:
    def test_info_con_tapizado(self, asiento):
        assert asiento.obtener_info_asiento() == (
            "Capacidad: 3 personas, Respaldo: Sí, Tapizado: cuero"
        )

    def test_info_sin_tapizado_ni_respaldo(self):
        asiento = AsientoConcreto("A", "Madera", "Café", 100.0, 1, False)
        assert asiento.obtener_info_asiento() == "Capacidad: 1 personas, Respaldo: No"
