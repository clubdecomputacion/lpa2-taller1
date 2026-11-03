"""
Pruebas de la clase Sillon.
Sillon no hereda de Asiento (el import está comentado en el código fuente),
así que se prueba como clase independiente.
"""

import pytest

from models.concretos.sillon import Sillon


@pytest.fixture
def sillon():
    return Sillon("Sillón Relax", "Madera", "Marrón", 500)


class TestSillonConstruccion:
    def test_valores_por_defecto(self, sillon):
        assert sillon.capacidad_personas == 2
        assert sillon.tiene_respaldo is True
        assert sillon.material_tapizado is None
        assert sillon.tiene_brazos is True
        assert sillon.es_reclinable is False
        assert sillon.tiene_reposapiés is False

    def test_precio_base_se_convierte_a_entero(self):
        assert Sillon("S", "Madera", "Café", 99.9).precio_base == 99

    def test_precio_base_none_es_cero(self):
        assert Sillon("S", "Madera", "Café", None).precio_base == 0


class TestSillonPrecio:
    def test_precio_por_defecto(self, sillon):
        # 500 + 100 (brazos)
        assert sillon.calcular_precio() == 600

    def test_precio_sin_brazos(self):
        assert Sillon("S", "Madera", "Café", 500, tiene_brazos=False).calcular_precio() == 500

    def test_precio_con_todos_los_extras(self):
        sillon = Sillon(
            "S",
            "Madera",
            "Café",
            500,
            material_tapizado="cuero",
            es_reclinable=True,
            tiene_reposapiés=True,
        )
        # 500 + 200 + 100 + 250 + 80
        assert sillon.calcular_precio() == 1130

    def test_precio_es_entero(self, sillon):
        assert isinstance(sillon.calcular_precio(), int)


class TestSillonDescripcion:
    def test_descripcion_sin_tapizado(self, sillon):
        desc = sillon.obtener_descripcion()
        assert desc.startswith("Sillón 'Sillón Relax'")
        assert "Tapizado=N/A" in desc
        assert "Brazos=Sí" in desc
        assert "Reclinable=No" in desc
        assert "Reposapiés=No" in desc
        assert "Precio base=$500" in desc

    def test_descripcion_con_extras(self):
        sillon = Sillon(
            "S",
            "Madera",
            "Café",
            500,
            material_tapizado="cuero",
            tiene_brazos=False,
            es_reclinable=True,
            tiene_reposapiés=True,
        )
        desc = sillon.obtener_descripcion()
        assert "Tapizado=cuero" in desc
        assert "Brazos=No" in desc
        assert "Reclinable=Sí" in desc
        assert "Reposapiés=Sí" in desc
