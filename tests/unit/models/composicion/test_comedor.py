"""
Pruebas de la clase Comedor (composición de una Mesa y varias Sillas).
"""

from unittest.mock import Mock

import pytest

from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


@pytest.fixture
def comedor_dos_sillas(mesa_basica, sillas_comedor):
    return Comedor("Pequeño", mesa_basica, sillas_comedor[:2])


class TestComedorComposicion:
    def test_contiene_mesa_y_sillas(self, comedor_completo, mesa_basica):
        assert comedor_completo.nombre == "Familiar"
        assert comedor_completo.mesa is mesa_basica
        assert len(comedor_completo.sillas) == 4

    def test_sin_sillas_crea_lista_vacia(self, mesa_basica):
        assert Comedor("Vacío", mesa_basica).sillas == []

    def test_sillas_devuelve_una_copia(self, comedor_completo):
        comedor_completo.sillas.clear()
        assert len(comedor_completo.sillas) == 4

    def test_len_cuenta_mesa_y_sillas(self, comedor_completo):
        assert len(comedor_completo) == 5

    def test_str(self, comedor_completo):
        assert str(comedor_completo) == "Comedor Familiar: Mesa + 4 sillas"


class TestComedorAgregarQuitar:
    def test_agregar_silla(self, comedor_dos_sillas, silla_basica):
        resultado = comedor_dos_sillas.agregar_silla(silla_basica)
        assert resultado == "Silla Silla Básica agregada exitosamente al comedor"
        assert len(comedor_dos_sillas.sillas) == 3

    def test_agregar_silla_supera_capacidad_de_la_mesa(self, comedor_completo, silla_basica):
        resultado = comedor_completo.agregar_silla(silla_basica)
        assert resultado == "No se pueden agregar más sillas. Capacidad máxima: 4"
        assert len(comedor_completo.sillas) == 4

    def test_agregar_objeto_que_no_es_silla(self, comedor_dos_sillas, mesa_basica):
        resultado = comedor_dos_sillas.agregar_silla(mesa_basica)
        assert resultado == "Error: Solo se pueden agregar objetos de tipo Silla"

    def test_capacidad_por_defecto_si_la_mesa_no_la_define(self, silla_basica):
        mesa = Mock(spec=["calcular_precio", "obtener_descripcion", "material"])
        comedor = Comedor("Mock", mesa, [silla_basica] * 6)
        resultado = comedor.agregar_silla(silla_basica)
        assert resultado == "No se pueden agregar más sillas. Capacidad máxima: 6"

    def test_quitar_ultima_silla(self, comedor_dos_sillas):
        resultado = comedor_dos_sillas.quitar_silla()
        assert resultado == "Silla Silla Comedor 2 removida del comedor"
        assert len(comedor_dos_sillas.sillas) == 1

    def test_quitar_silla_por_indice(self, comedor_dos_sillas):
        assert comedor_dos_sillas.quitar_silla(0) == "Silla Silla Comedor 1 removida del comedor"

    def test_quitar_silla_indice_invalido(self, comedor_dos_sillas):
        assert comedor_dos_sillas.quitar_silla(10) == "Índice de silla inválido"

    def test_quitar_silla_sin_sillas(self, mesa_basica):
        assert Comedor("Vacío", mesa_basica).quitar_silla() == "No hay sillas para quitar"


class TestComedorPrecio:
    def test_precio_sin_descuento(self, comedor_dos_sillas):
        # 104.8 + 2 * 120
        assert comedor_dos_sillas.calcular_precio_total() == pytest.approx(344.8)

    def test_precio_con_descuento_desde_4_sillas(self, comedor_completo):
        # (104.8 + 4 * 120) * 0.95
        assert comedor_completo.calcular_precio_total() == pytest.approx(555.56)

    def test_precio_usa_los_componentes(self):
        mesa = Mock(spec=Mesa)
        mesa.calcular_precio.return_value = 200.0
        silla = Mock(spec=Silla)
        silla.calcular_precio.return_value = 50.0

        comedor = Comedor("Mock", mesa, [silla, silla])

        assert comedor.calcular_precio_total() == 300.0
        mesa.calcular_precio.assert_called_once()
        assert silla.calcular_precio.call_count == 2


class TestComedorDescripcionYResumen:
    def test_descripcion_completa_con_descuento(self, comedor_completo):
        desc = comedor_completo.obtener_descripcion_completa()
        assert desc.startswith("=== COMEDOR FAMILIAR ===")
        assert "MESA:\nMesa: Mesa Básica" in desc
        assert "SILLAS (4 unidades):" in desc
        assert "1. Silla: Silla Comedor 1" in desc
        assert "--- PRECIO TOTAL: $555.56 ---" in desc
        assert "(Incluye 5% de descuento por set completo)" in desc

    def test_descripcion_completa_sin_sillas(self, mesa_basica):
        desc = Comedor("Vacío", mesa_basica).obtener_descripcion_completa()
        assert "SILLAS: Ninguna incluida" in desc
        assert "descuento" not in desc

    def test_resumen(self, comedor_dos_sillas):
        resumen = comedor_dos_sillas.obtener_resumen()
        assert resumen["nombre"] == "Pequeño"
        assert resumen["total_muebles"] == 3
        assert resumen["precio_mesa"] == pytest.approx(104.8)
        assert resumen["precio_sillas"] == pytest.approx(240.0)
        assert resumen["precio_total"] == pytest.approx(344.8)
        assert resumen["capacidad_personas"] == 2
        assert sorted(resumen["materiales_utilizados"]) == ["Madera", "Roble", "tela"]

    def test_resumen_sin_tapizado(self, mesa_basica, silla_basica):
        resumen = Comedor("Simple", mesa_basica, [silla_basica]).obtener_resumen()
        assert sorted(resumen["materiales_utilizados"]) == ["Madera", "Roble"]
