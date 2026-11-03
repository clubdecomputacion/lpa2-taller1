"""
Pruebas de la clase Silla.
"""

import pytest

from models.categorias.asientos import Asiento
from models.concretos.silla import Silla


class TestSillaConstruccion:
    def test_hereda_de_asiento(self, silla_basica):
        assert isinstance(silla_basica, Asiento)

    def test_valores_por_defecto(self, silla_basica):
        assert silla_basica.capacidad_personas == 1
        assert silla_basica.tiene_respaldo is True
        assert silla_basica.material_tapizado is None
        assert silla_basica.altura_regulable is False
        assert silla_basica.tiene_ruedas is False

    def test_setters(self, silla_basica):
        silla_basica.altura_regulable = True
        silla_basica.tiene_ruedas = True
        assert silla_basica.altura_regulable is True
        assert silla_basica.tiene_ruedas is True


class TestSillaPrecio:
    def test_precio_silla_basica(self, silla_basica):
        assert silla_basica.calcular_precio() == pytest.approx(110.0)

    def test_precio_silla_oficina(self, silla_oficina):
        # 100 * 1.3 (respaldo + cuero) + 30 (altura) + 20 (ruedas)
        assert silla_oficina.calcular_precio() == pytest.approx(180.0)

    @pytest.mark.parametrize(
        "respaldo,tapizado,esperado",
        [
            (False, None, 100.0),
            (True, "tela", 120.0),
            (True, "cuero", 130.0),
        ],
    )
    def test_precio_segun_comodidad(self, respaldo, tapizado, esperado):
        silla = Silla("S", "Madera", "Café", 100.0, respaldo, tapizado)
        assert silla.calcular_precio() == pytest.approx(esperado)

    def test_precio_se_redondea_a_dos_decimales(self):
        silla = Silla("S", "Madera", "Café", 33.333)
        assert silla.calcular_precio() == round(33.333 * 1.1, 2)


class TestSillaComportamiento:
    def test_regular_altura_sin_mecanismo(self, silla_basica):
        assert silla_basica.regular_altura(60) == "Esta silla no tiene altura regulable"

    @pytest.mark.parametrize("altura", [40, 70, 100])
    def test_regular_altura_valida(self, silla_oficina, altura):
        assert silla_oficina.regular_altura(altura) == f"Altura ajustada a {altura} cm"

    @pytest.mark.parametrize("altura", [39, 101])
    def test_regular_altura_fuera_de_rango(self, silla_oficina, altura):
        assert silla_oficina.regular_altura(altura) == "La altura debe estar entre 40 y 100 cm"

    def test_es_silla_oficina(self, silla_basica, silla_oficina):
        assert silla_oficina.es_silla_oficina() is True
        assert silla_basica.es_silla_oficina() is False

    def test_solo_ruedas_no_es_silla_oficina(self):
        silla = Silla("S", "Metal", "Negro", 100.0, tiene_ruedas=True)
        assert silla.es_silla_oficina() is False

    def test_descripcion(self, silla_oficina):
        desc = silla_oficina.obtener_descripcion()
        assert desc.startswith("Silla: Silla Oficina")
        assert "Material: Metal" in desc
        assert "Tapizado: cuero" in desc
        assert "Altura regulable: Sí" in desc
        assert "Ruedas: Sí" in desc
        assert "Precio final: $180.0" in desc

    def test_descripcion_sin_extras(self, silla_basica):
        desc = silla_basica.obtener_descripcion()
        assert "Altura regulable: No" in desc
        assert "Ruedas: No" in desc
