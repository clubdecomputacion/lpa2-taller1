"""
Pruebas de la clase Cajonera.
Cajonera no hereda de Almacenamiento (el import está comentado en el código fuente).
"""

import pytest

from models.concretos.cajonera import Cajonera


@pytest.fixture
def cajonera():
    return Cajonera("Cajonera Básica", "Madera", "Blanco", 200)


class TestCajoneraConstruccion:
    def test_valores_por_defecto(self, cajonera):
        assert cajonera.num_cajones == 3
        assert cajonera.tiene_ruedas is False

    def test_precio_base_se_convierte_a_entero(self):
        assert Cajonera("C", "Madera", "Café", 199.99).precio_base == 199

    def test_precio_base_none_es_cero(self):
        assert Cajonera("C", "Madera", "Café", None).precio_base == 0


class TestCajoneraPrecio:
    def test_precio_por_defecto(self, cajonera):
        # 200 + 3 cajones * 20
        assert cajonera.calcular_precio() == 260

    @pytest.mark.parametrize(
        "cajones,ruedas,esperado",
        [(0, False, 200), (5, False, 300), (5, True, 330)],
    )
    def test_precio_con_componentes(self, cajones, ruedas, esperado):
        assert Cajonera("C", "Madera", "Café", 200, cajones, ruedas).calcular_precio() == esperado


class TestCajoneraDescripcion:
    def test_descripcion(self, cajonera):
        desc = cajonera.obtener_descripcion()
        assert desc.startswith("Cajonera 'Cajonera Básica'")
        assert "Cajones=3" in desc
        assert "Ruedas=No" in desc
        assert "Precio base=$200" in desc

    def test_descripcion_con_ruedas(self):
        assert "Ruedas=Sí" in Cajonera("C", "Madera", "Café", 200, tiene_ruedas=True).obtener_descripcion()
