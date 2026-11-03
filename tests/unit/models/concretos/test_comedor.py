"""
Pruebas de la clase Comedor de models/concretos (versión simple, sin descuento).
"""

import pytest

from models.concretos.comedor import Comedor


@pytest.fixture
def comedor(mesa_basica, silla_basica):
    return Comedor(mesa_basica, [silla_basica])


class TestComedorSimple:
    def test_sin_sillas_crea_lista_vacia(self, mesa_basica):
        comedor = Comedor(mesa_basica)
        assert comedor.sillas == []
        assert comedor.cantidad_sillas() == 0

    def test_precio_total_sin_descuento(self, mesa_basica, sillas_comedor):
        comedor = Comedor(mesa_basica, sillas_comedor)
        # 104.8 + 4 * 120
        assert comedor.calcular_precio_total() == pytest.approx(584.8)

    def test_agregar_silla(self, comedor, silla_oficina):
        comedor.agregar_silla(silla_oficina)
        assert comedor.cantidad_sillas() == 2

    def test_quitar_silla_existente(self, comedor, silla_basica):
        comedor.quitar_silla(silla_basica)
        assert comedor.cantidad_sillas() == 0

    def test_quitar_silla_inexistente_no_hace_nada(self, comedor, silla_oficina):
        comedor.quitar_silla(silla_oficina)
        assert comedor.cantidad_sillas() == 1

    def test_descripcion(self, comedor):
        desc = comedor.descripcion()
        assert desc.startswith("Comedor con mesa: Mesa: Mesa Básica")
        assert "y 1 sillas:" in desc
        assert "1. Silla: Silla Básica" in desc
