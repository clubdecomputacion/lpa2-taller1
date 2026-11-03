"""
Pruebas de la clase Cama.
"""

import pytest

from models.mueble import Mueble
from models.concretos.cama import Cama


class TestCamaConstruccion:
    def test_hereda_de_mueble(self, cama_basica):
        assert isinstance(cama_basica, Mueble)

    def test_valores_por_defecto(self, cama_basica):
        assert cama_basica.tamaño == "individual"
        assert cama_basica.incluye_colchon is False
        assert cama_basica.tiene_cabecera is False

    @pytest.mark.parametrize("tamaño", ["individual", "matrimonial", "queen", "king"])
    def test_setter_tamaño_valido(self, cama_basica, tamaño):
        cama_basica.tamaño = tamaño
        assert cama_basica.tamaño == tamaño

    def test_setter_tamaño_invalido_lanza_error(self, cama_basica):
        with pytest.raises(ValueError, match="Tamaño debe ser uno de"):
            cama_basica.tamaño = "gigante"


class TestCamaPrecio:
    @pytest.mark.parametrize(
        "tamaño,esperado",
        [("individual", 500.0), ("matrimonial", 700.0), ("queen", 900.0), ("king", 1100.0)],
    )
    def test_precio_por_tamaño(self, tamaño, esperado):
        assert Cama("C", "Madera", "Blanco", 500.0, tamaño).calcular_precio() == esperado

    def test_precio_con_colchon_y_cabecera(self):
        cama = Cama("C", "Madera", "Blanco", 500.0, "king", incluye_colchon=True, tiene_cabecera=True)
        # 500 + 600 + 300 + 100
        assert cama.calcular_precio() == 1500.0


class TestCamaDescripcion:
    def test_descripcion(self, cama_basica):
        desc = cama_basica.obtener_descripcion()
        assert desc.startswith("Cama: Cama Básica")
        assert "Tamaño: individual" in desc
        assert "Incluye colchón: No" in desc
        assert "Cabecera: No" in desc
        assert "Precio final: $500.0" in desc

    def test_descripcion_con_extras(self):
        cama = Cama("C", "Madera", "Blanco", 500.0, incluye_colchon=True, tiene_cabecera=True)
        desc = cama.obtener_descripcion()
        assert "Incluye colchón: Sí" in desc
        assert "Cabecera: Sí" in desc
