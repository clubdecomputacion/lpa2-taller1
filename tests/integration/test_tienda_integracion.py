"""
Pruebas de integración: la tienda trabajando con los modelos reales y con
los datos de ejemplo que arma main.py.
"""

from unittest.mock import patch

import pytest

import main
from services.tienda import TiendaMuebles

pytestmark = pytest.mark.integration


@pytest.fixture
def tienda_demo(capsys):
    """Tienda con el catálogo, comedores y descuentos de ejemplo de main.py."""
    tienda = TiendaMuebles("Mueblería Demo")
    main.crear_catalogo_inicial(tienda)
    main.crear_comedores_ejemplo(tienda)
    main.aplicar_descuentos_ejemplo(tienda)
    capsys.readouterr()  # descarta lo impreso durante la preparación
    return tienda


class TestCatalogoDeEjemplo:
    def test_carga_todo_el_catalogo(self, tienda_demo):
        stats = tienda_demo.obtener_estadisticas()
        assert stats["total_muebles"] == 17
        assert stats["total_comedores"] == 2
        assert stats["descuentos_activos"] == {"Silla": 0.1, "Mesa": 0.15, "Sofa": 0.2}
        assert stats["tipos_muebles"]["SofaCama"] == 1

    def test_inventario_valorizado(self, tienda_demo):
        stats = tienda_demo.obtener_estadisticas()
        suma = sum(m.calcular_precio() for m in tienda_demo._inventario)
        assert stats["valor_inventario"] == pytest.approx(suma)
        assert stats["valor_inventario"] > 0

    def test_buscar_y_filtrar_sobre_catalogo(self, tienda_demo):
        sillas = tienda_demo.buscar_muebles_por_nombre("silla")
        assert len(sillas) == 3
        assert all(m.material.lower() == "madera" for m in tienda_demo.filtrar_por_material("MADERA"))
        baratos = tienda_demo.filtrar_por_precio(0, 200)
        assert all(m.calcular_precio() <= 200 for m in baratos)

    def test_mostrar_estadisticas_iniciales(self, tienda_demo, capsys):
        main.mostrar_estadisticas_iniciales(tienda_demo)
        salida = capsys.readouterr().out
        assert "Total de muebles: 17" in salida
        assert "Total de comedores: 2" in salida
        assert "SofaCama: 1 unidades" in salida


class TestFlujoDeVentas:
    def test_venta_con_descuento_de_categoria(self, tienda_demo):
        silla = tienda_demo.buscar_muebles_por_nombre("Silla Clásica")[0]

        venta = tienda_demo.realizar_venta(silla, "Cliente Integración")

        # 150 * 1.2 (respaldo + tela) = 180, con 10% de descuento
        assert venta["precio_original"] == pytest.approx(180.0)
        assert venta["precio_final"] == pytest.approx(162.0)
        assert tienda_demo.buscar_muebles_por_nombre("Silla Clásica") == []

    def test_descuento_aplica_solo_a_la_clase_exacta(self, tienda_demo):
        # El descuento de "Sofa" no se aplica a SofaCama aunque herede de Sofa
        sofacama = tienda_demo.buscar_muebles_por_nombre("SofaCama")[0]
        assert tienda_demo.realizar_venta(sofacama)["descuento"] == 0

    def test_varias_ventas_acumulan_estadisticas(self, tienda_demo):
        muebles = tienda_demo.filtrar_por_precio(0, 300)[:3]
        ventas = [tienda_demo.realizar_venta(m) for m in muebles]

        stats = tienda_demo.obtener_estadisticas()
        assert stats["total_muebles"] == 17 - len(muebles)
        assert stats["ventas_realizadas"] == len(muebles)
        assert stats["total_muebles_vendidos"] == len(muebles)
        assert stats["valor_total_ventas"] == pytest.approx(sum(v["precio_final"] for v in ventas))

    def test_reporte_refleja_el_estado(self, tienda_demo):
        reporte = tienda_demo.generar_reporte_inventario()
        assert "Mueblería Demo" in reporte
        assert "Total de muebles: 17" in reporte
        assert "- Sofa: 20.0%" in reporte


class TestMain:
    @patch("main.MenuTienda")
    @patch("builtins.input", return_value="")
    def test_main_inicia_el_menu(self, mock_input, mock_menu, capsys):
        main.main()

        mock_menu.assert_called_once()
        tienda = mock_menu.call_args.args[0]
        assert tienda.nombre == "Mueblería Moderna OOP"
        mock_menu.return_value.ejecutar.assert_called_once()
        assert "Programa finalizado" in capsys.readouterr().out

    @patch("main.MenuTienda")
    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_main_interrumpido_por_el_usuario(self, mock_input, mock_menu, capsys):
        main.main()

        mock_menu.return_value.ejecutar.assert_not_called()
        salida = capsys.readouterr().out
        assert "Programa interrumpido por el usuario" in salida
        assert "Programa finalizado" in salida

    @patch("main.MenuTienda")
    @patch("builtins.input", return_value="")
    def test_main_maneja_errores_inesperados(self, mock_input, mock_menu, capsys):
        mock_menu.return_value.ejecutar.side_effect = RuntimeError("fallo del menú")

        main.main()

        salida = capsys.readouterr().out
        assert "Error inesperado: fallo del menú" in salida
        assert "Programa finalizado" in salida
