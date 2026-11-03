"""
Pruebas de la clase abstracta Mueble.
"""

import pytest

from models.mueble import Mueble


class TestMuebleAbstracto:
    def test_no_se_puede_instanciar(self):
        with pytest.raises(TypeError):
            Mueble("Mesa", "Madera", "Café", 100.0)

    def test_define_metodos_abstractos(self):
        assert Mueble.__abstractmethods__ == {"calcular_precio", "obtener_descripcion"}

    def test_subclase_incompleta_no_se_puede_instanciar(self):
        class MuebleIncompleto(Mueble):
            def calcular_precio(self):
                return 0

        with pytest.raises(TypeError):
            MuebleIncompleto("X", "Madera", "Café", 10.0)


class TestMuebleAtributos:
    def test_constructor_asigna_atributos(self, mueble):
        assert mueble.nombre == "Mueble Prueba"
        assert mueble.material == "Madera"
        assert mueble.color == "Café"
        assert mueble.precio_base == 100.0

    @pytest.mark.parametrize("atributo", ["nombre", "material", "color"])
    def test_setter_texto_quita_espacios(self, mueble, atributo):
        setattr(mueble, atributo, "  Valor  ")
        assert getattr(mueble, atributo) == "Valor"

    @pytest.mark.parametrize("atributo", ["nombre", "material", "color"])
    @pytest.mark.parametrize("valor", ["", "   ", None])
    def test_setter_texto_vacio_lanza_error(self, mueble, atributo, valor):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            setattr(mueble, atributo, valor)

    def test_precio_base_acepta_cero(self, mueble):
        mueble.precio_base = 0
        assert mueble.precio_base == 0

    def test_precio_base_negativo_lanza_error(self, mueble):
        with pytest.raises(ValueError, match="no puede ser negativo"):
            mueble.precio_base = -1


class TestMuebleRepresentacion:
    def test_str(self, mueble):
        assert str(mueble) == "Mueble Prueba de Madera en color Café"

    def test_repr(self, mueble):
        assert repr(mueble) == (
            "Mueble(nombre='Mueble Prueba', material='Madera', "
            "color='Café', precio_base=100.0)"
        )
