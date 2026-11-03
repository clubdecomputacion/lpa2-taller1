"""
Pruebas de la clase Escritorio.
Escritorio no hereda de Mueble (el import está comentado en el código fuente).
"""

import pytest

from models.concretos.escritorio import Escritorio


@pytest.fixture
def escritorio():
    return Escritorio("Escritorio Simple", "Madera", "Blanco", 300)


class TestEscritorioConstruccion:
    def test_valores_por_defecto(self, escritorio):
        assert escritorio.forma == "rectangular"
        assert escritorio.tiene_cajones is False
        assert escritorio.num_cajones == 0
        assert escritorio.largo == 1.2
        assert escritorio.tiene_iluminacion is False

    def test_precio_base_se_convierte_a_entero(self):
        assert Escritorio("E", "Madera", "Café", 250.7).precio_base == 250

    def test_precio_base_none_es_cero(self):
        assert Escritorio("E", "Madera", "Café", None).precio_base == 0


class TestEscritorioPrecio:
    def test_precio_basico(self, escritorio):
        assert escritorio.calcular_precio() == 300

    def test_cajones_suman_25_cada_uno(self):
        escritorio = Escritorio("E", "Madera", "Café", 300, tiene_cajones=True, num_cajones=3)
        assert escritorio.calcular_precio() == 375

    def test_cajones_sin_flag_no_suman(self):
        escritorio = Escritorio("E", "Madera", "Café", 300, tiene_cajones=False, num_cajones=3)
        assert escritorio.calcular_precio() == 300

    @pytest.mark.parametrize("largo,esperado", [(1.5, 300), (1.6, 350)])
    def test_extra_por_largo(self, largo, esperado):
        assert Escritorio("E", "Madera", "Café", 300, largo=largo).calcular_precio() == esperado

    def test_iluminacion_suma_40(self):
        assert Escritorio("E", "Madera", "Café", 300, tiene_iluminacion=True).calcular_precio() == 340

    def test_forma_no_rectangular_suma_30(self):
        assert Escritorio("E", "Madera", "Café", 300, forma="L").calcular_precio() == 330


class TestEscritorioDescripcion:
    def test_descripcion_sin_cajones(self, escritorio):
        desc = escritorio.obtener_descripcion()
        assert desc.startswith("Escritorio 'Escritorio Simple'")
        assert "Forma=rectangular" in desc
        assert "Cajones=0" in desc
        assert "Largo=1.2m" in desc
        assert "Iluminación=No" in desc
        assert "Precio base=$300" in desc

    def test_descripcion_con_cajones_e_iluminacion(self):
        escritorio = Escritorio(
            "E", "Madera", "Café", 300, tiene_cajones=True, num_cajones=4, tiene_iluminacion=True
        )
        desc = escritorio.obtener_descripcion()
        assert "Cajones=4" in desc
        assert "Iluminación=Sí" in desc
