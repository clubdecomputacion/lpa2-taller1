"""
Pruebas de la clase Sofa.
"""

import pytest

from models.categorias.asientos import Asiento
from models.concretos.sofa import Sofa


class TestSofaConstruccion:
    def test_hereda_de_asiento(self, sofa_basico):
        assert isinstance(sofa_basico, Asiento)

    def test_valores_por_defecto(self, sofa_basico):
        assert sofa_basico.capacidad_personas == 3
        assert sofa_basico.tiene_respaldo is True
        assert sofa_basico.tiene_brazos is True
        assert sofa_basico.es_modular is False
        assert sofa_basico.incluye_cojines is False


class TestSofaPrecio:
    def test_precio_sofa_basico(self, sofa_basico):
        # 100 * 1.2 (respaldo + 3 personas) + 150 (brazos)
        assert sofa_basico.calcular_precio() == pytest.approx(270.0)

    @pytest.mark.parametrize(
        "brazos,modular,cojines,esperado",
        [
            (False, False, False, 120.0),
            (True, True, False, 470.0),
            (True, False, True, 320.0),
            (True, True, True, 520.0),
        ],
    )
    def test_precio_con_extras(self, brazos, modular, cojines, esperado):
        sofa = Sofa(
            "S",
            "Tela",
            "Gris",
            100.0,
            tiene_brazos=brazos,
            es_modular=modular,
            incluye_cojines=cojines,
        )
        assert sofa.calcular_precio() == pytest.approx(esperado)

    def test_precio_con_tapizado_de_cuero(self):
        sofa = Sofa("S", "Tela", "Gris", 100.0, material_tapizado="cuero")
        assert sofa.calcular_precio() == pytest.approx(290.0)


class TestSofaDescripcion:
    def test_descripcion(self, sofa_basico):
        desc = sofa_basico.obtener_descripcion()
        assert desc.startswith("Sofá: Sofá Básico")
        assert "Capacidad: 3 personas" in desc
        assert "Brazos: Sí" in desc
        assert "Modular: No" in desc
        assert "Incluye cojines: No" in desc
        assert "Precio final: $270.0" in desc

    def test_descripcion_con_todos_los_extras(self):
        sofa = Sofa("S", "Tela", "Gris", 100.0, tiene_brazos=False, es_modular=True, incluye_cojines=True)
        desc = sofa.obtener_descripcion()
        assert "Brazos: No" in desc
        assert "Modular: Sí" in desc
        assert "Incluye cojines: Sí" in desc
