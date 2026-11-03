"""
Pruebas de la clase Mesa.
"""

import pytest

from models.categorias.superficies import Superficie
from models.concretos.mesa import Mesa


class TestMesaConstruccion:
    def test_hereda_de_superficie(self, mesa_basica):
        assert isinstance(mesa_basica, Superficie)

    def test_valores_por_defecto(self, mesa_basica):
        assert mesa_basica.forma == "rectangular"
        assert (mesa_basica.largo, mesa_basica.ancho, mesa_basica.altura) == (120.0, 80.0, 75.0)
        assert mesa_basica.capacidad_personas == 4

    @pytest.mark.parametrize("forma", ["rectangular", "redonda", "cuadrada", "ovalada"])
    def test_setter_forma_valida(self, mesa_basica, forma):
        mesa_basica.forma = forma
        assert mesa_basica.forma == forma

    def test_setter_forma_invalida_lanza_error(self, mesa_basica):
        with pytest.raises(ValueError, match="Forma debe ser una de"):
            mesa_basica.forma = "triangular"

    def test_setter_capacidad(self, mesa_basica):
        mesa_basica.capacidad_personas = 6
        assert mesa_basica.capacidad_personas == 6

    @pytest.mark.parametrize("valor", [0, -3])
    def test_setter_capacidad_invalida_lanza_error(self, mesa_basica, valor):
        with pytest.raises(ValueError, match="mayor a 0"):
            mesa_basica.capacidad_personas = valor


class TestMesaPrecio:
    def test_precio_mesa_basica(self, mesa_basica):
        # 100 * (1 + 9600/10000 * 0.05) = 104.8
        assert mesa_basica.calcular_precio() == pytest.approx(104.8)

    def test_forma_no_rectangular_suma_50(self):
        mesa = Mesa("M", "Roble", "Natural", 100.0, forma="redonda")
        assert mesa.calcular_precio() == pytest.approx(154.8)

    @pytest.mark.parametrize(
        "capacidad,extra",
        [(4, 0), (5, 50), (6, 50), (7, 100), (10, 100)],
    )
    def test_extra_por_capacidad(self, capacidad, extra):
        mesa = Mesa("M", "Roble", "Natural", 100.0, capacidad_personas=capacidad)
        assert mesa.calcular_precio() == pytest.approx(104.8 + extra)


class TestMesaDescripcion:
    def test_descripcion(self, mesa_basica):
        desc = mesa_basica.obtener_descripcion()
        assert desc.startswith("Mesa: Mesa Básica")
        assert "Forma: rectangular" in desc
        assert "Dimensiones: 120.0x80.0x75.0cm" in desc
        assert "Capacidad: 4 personas" in desc
        assert "Precio final: $104.8" in desc
