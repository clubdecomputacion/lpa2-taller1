"""
Pruebas de la clase abstracta Superficie.
"""

import pytest

from models.mueble import Mueble
from models.categorias.superficies import Superficie


class TestSuperficieAbstracta:
    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Superficie("Mesa", "Madera", "Café", 100.0, 100, 80, 75)

    def test_hereda_de_mueble(self, superficie):
        assert isinstance(superficie, Mueble)


class TestSuperficieDimensiones:
    def test_constructor_asigna_dimensiones(self, superficie):
        assert (superficie.largo, superficie.ancho, superficie.altura) == (100.0, 100.0, 75.0)

    @pytest.mark.parametrize("atributo", ["largo", "ancho", "altura"])
    def test_setter_valido(self, superficie, atributo):
        setattr(superficie, atributo, 50.0)
        assert getattr(superficie, atributo) == 50.0

    @pytest.mark.parametrize("atributo", ["largo", "ancho", "altura"])
    @pytest.mark.parametrize("valor", [0, -1])
    def test_setter_invalido_lanza_error(self, superficie, atributo, valor):
        with pytest.raises(ValueError, match="debe ser mayor a 0"):
            setattr(superficie, atributo, valor)


class TestSuperficieCalculos:
    def test_calcular_area(self, superficie):
        assert superficie.calcular_area() == 10000.0

    def test_factor_tamaño(self, superficie):
        assert superficie.calcular_factor_tamaño() == pytest.approx(1.05)

    def test_factor_tamaño_crece_con_el_area(self, superficie):
        superficie.largo = 200.0
        assert superficie.calcular_factor_tamaño() == pytest.approx(1.10)

    def test_info_superficie(self, superficie):
        assert superficie.obtener_info_superficie() == (
            "Dimensiones: 100.0x100.0x75.0cm (Área: 10000.0cm²)"
        )
