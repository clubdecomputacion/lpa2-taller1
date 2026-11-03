"""
Pruebas de la clase Armario.
Armario no hereda de Almacenamiento (el import está comentado en el código fuente).
"""

import pytest

from models.concretos.armario import Armario


@pytest.fixture
def armario():
    return Armario("Armario Clásico", "Madera", "Café", 800)


class TestArmarioConstruccion:
    def test_valores_por_defecto(self, armario):
        assert armario.num_puertas == 2
        assert armario.num_cajones == 0
        assert armario.tiene_espejos is False

    def test_precio_base_se_convierte_a_entero(self):
        assert Armario("A", "Madera", "Café", 800.9).precio_base == 800

    def test_precio_base_none_es_cero(self):
        assert Armario("A", "Madera", "Café", None).precio_base == 0


class TestArmarioPrecio:
    def test_precio_por_defecto(self, armario):
        # 800 + 2 puertas * 50
        assert armario.calcular_precio() == 900

    @pytest.mark.parametrize(
        "puertas,cajones,espejos,esperado",
        [
            (0, 0, False, 800),
            (3, 2, False, 1010),
            (4, 4, True, 1220),
        ],
    )
    def test_precio_con_componentes(self, puertas, cajones, espejos, esperado):
        armario = Armario("A", "Madera", "Café", 800, puertas, cajones, espejos)
        assert armario.calcular_precio() == esperado


class TestArmarioDescripcion:
    def test_descripcion(self, armario):
        desc = armario.obtener_descripcion()
        assert desc.startswith("Armario 'Armario Clásico'")
        assert "Puertas=2" in desc
        assert "Cajones=0" in desc
        assert "Espejos=No" in desc
        assert "Precio base=$800" in desc

    def test_descripcion_con_espejos(self):
        assert "Espejos=Sí" in Armario("A", "Madera", "Café", 800, tiene_espejos=True).obtener_descripcion()
