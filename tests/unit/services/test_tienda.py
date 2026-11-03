"""
Pruebas del servicio TiendaMuebles.
"""

from unittest.mock import Mock, PropertyMock, patch

import pytest

from models.concretos.silla import Silla
from models.concretos.mesa import Mesa


def mueble_con_fallo(nombre="Roto", precio_inicial=100.0):
    """Mock de mueble cuyo precio funciona una vez y luego falla."""
    mueble = Mock()
    mueble.nombre = nombre
    mueble.material = "Madera"
    mueble.calcular_precio.side_effect = [precio_inicial, RuntimeError("falla")]
    return mueble


@pytest.fixture
def tienda_con_muebles(tienda, silla_basica, silla_oficina, mesa_basica):
    for mueble in (silla_basica, silla_oficina, mesa_basica):
        tienda.agregar_mueble(mueble)
    return tienda


class TestTiendaCreacion:
    def test_nombre_por_defecto(self):
        from services.tienda import TiendaMuebles

        assert TiendaMuebles().nombre == "Mueblería OOP"

    def test_nombre_personalizado(self, tienda):
        assert tienda.nombre == "Tienda de Prueba"

    def test_inicia_vacia(self, tienda):
        stats = tienda.obtener_estadisticas()
        assert stats["total_muebles"] == 0
        assert stats["total_comedores"] == 0
        assert stats["ventas_realizadas"] == 0


class TestAgregar:
    def test_agregar_mueble(self, tienda, silla_basica):
        resultado = tienda.agregar_mueble(silla_basica)
        assert resultado == "Mueble Silla Básica agregado exitosamente al inventario"
        assert tienda.obtener_estadisticas()["total_muebles"] == 1

    def test_agregar_none(self, tienda):
        assert tienda.agregar_mueble(None) == "Error: El mueble no puede ser None"

    def test_agregar_mueble_con_precio_cero(self, tienda):
        silla = Silla("Gratis", "Madera", "Café", 0.0)
        resultado = tienda.agregar_mueble(silla)
        assert resultado == "Error: El mueble debe tener un precio válido mayor a 0"
        assert tienda.obtener_estadisticas()["total_muebles"] == 0

    def test_agregar_mueble_cuyo_precio_falla(self, tienda):
        mueble = Mock()
        mueble.calcular_precio.side_effect = ValueError("sin precio")
        resultado = tienda.agregar_mueble(mueble)
        assert resultado == "Error al calcular precio del mueble: sin precio"

    def test_agregar_comedor(self, tienda, comedor_completo):
        assert tienda.agregar_comedor(comedor_completo) == "Comedor Familiar agregado exitosamente"
        assert tienda.obtener_estadisticas()["total_comedores"] == 1

    def test_agregar_comedor_none(self, tienda):
        assert tienda.agregar_comedor(None) == "Error: El comedor no puede ser None"


class TestBusquedaYFiltros:
    def test_buscar_por_nombre_parcial_sin_mayusculas(self, tienda_con_muebles):
        resultados = tienda_con_muebles.buscar_muebles_por_nombre("  SILLA ")
        assert [m.nombre for m in resultados] == ["Silla Básica", "Silla Oficina"]

    @pytest.mark.parametrize("texto", ["", "   ", None])
    def test_buscar_texto_vacio(self, tienda_con_muebles, texto):
        assert tienda_con_muebles.buscar_muebles_por_nombre(texto) == []

    def test_buscar_sin_coincidencias(self, tienda_con_muebles):
        assert tienda_con_muebles.buscar_muebles_por_nombre("armario") == []

    def test_filtrar_por_precio_rango_inclusivo(self, tienda_con_muebles):
        # Precios: silla básica 110, silla oficina 180, mesa 104.8
        resultados = tienda_con_muebles.filtrar_por_precio(104.8, 110.0)
        assert {m.nombre for m in resultados} == {"Silla Básica", "Mesa Básica"}

    def test_filtrar_por_precio_sin_limites(self, tienda_con_muebles):
        assert len(tienda_con_muebles.filtrar_por_precio()) == 3

    def test_filtrar_por_precio_minimo_negativo_se_ajusta_a_cero(self, tienda_con_muebles):
        assert len(tienda_con_muebles.filtrar_por_precio(-50, 1000)) == 3

    def test_filtrar_por_precio_salta_muebles_con_error(self, tienda, silla_basica):
        tienda.agregar_mueble(silla_basica)
        tienda.agregar_mueble(mueble_con_fallo())
        assert tienda.filtrar_por_precio() == [silla_basica]

    def test_filtrar_por_material(self, tienda_con_muebles):
        resultados = tienda_con_muebles.filtrar_por_material(" madera ")
        assert [m.nombre for m in resultados] == ["Silla Básica"]

    @pytest.mark.parametrize("material", ["", "  ", None])
    def test_filtrar_por_material_vacio(self, tienda_con_muebles, material):
        assert tienda_con_muebles.filtrar_por_material(material) == []

    def test_filtrar_por_material_salta_muebles_con_error(self, tienda, silla_basica):
        tienda.agregar_mueble(silla_basica)
        roto = Mock()
        type(roto).material = PropertyMock(side_effect=RuntimeError("falla"))
        tienda._inventario.append(roto)
        assert tienda.filtrar_por_material("Madera") == [silla_basica]


class TestMetodosPendientes:
    """
    Métodos que en el código fuente están marcados con TODO y retornan None.
    Se dejan como xfail estricto: si alguien los implementa, la prueba pasará
    y pytest avisará para quitar el marcador.
    """

    @pytest.mark.xfail(reason="TODO en src: obtener_muebles_por_tipo no implementado", strict=True)
    def test_obtener_muebles_por_tipo(self, tienda_con_muebles):
        assert len(tienda_con_muebles.obtener_muebles_por_tipo(Silla)) == 2

    @pytest.mark.xfail(reason="TODO en src: calcular_valor_inventario no implementado", strict=True)
    def test_calcular_valor_inventario(self, tienda_con_muebles):
        assert tienda_con_muebles.calcular_valor_inventario() == pytest.approx(394.8)

    @pytest.mark.xfail(reason="TODO en src: _contar_tipos_muebles no implementado", strict=True)
    def test_contar_tipos_muebles(self, tienda_con_muebles):
        assert tienda_con_muebles._contar_tipos_muebles() == {"Silla": 2, "Mesa": 1}


class TestDescuentos:
    @pytest.mark.parametrize(
        "categoria,clave",
        [("sillas", "Silla"), ("Mesa", "Mesa"), ("  SOFAS ", "Sofa")],
    )
    def test_aplicar_descuento_normaliza_categoria(self, tienda, categoria, clave):
        resultado = tienda.aplicar_descuento(categoria, 10)
        assert resultado == f"Descuento del 10% aplicado a la categoría '{clave}'"
        assert tienda.obtener_estadisticas()["descuentos_activos"] == {clave: 0.1}

    @pytest.mark.parametrize("porcentaje", [0, -5, 101])
    def test_aplicar_descuento_porcentaje_invalido(self, tienda, porcentaje):
        assert tienda.aplicar_descuento("sillas", porcentaje) == (
            "Error: El porcentaje debe estar entre 1 y 100"
        )
        assert tienda.obtener_estadisticas()["descuentos_activos"] == {}

    def test_aplicar_descuento_del_100(self, tienda):
        tienda.aplicar_descuento("mesa", 100)
        assert tienda.obtener_estadisticas()["descuentos_activos"] == {"Mesa": 1.0}


class TestVentas:
    @patch("datetime.datetime")
    def test_realizar_venta(self, mock_datetime, tienda, silla_basica):
        mock_datetime.now.return_value.strftime.return_value = "2026-01-15 10:30:00"
        tienda.agregar_mueble(silla_basica)

        venta = tienda.realizar_venta(silla_basica, "Ana")

        assert venta == {
            "mueble": "Silla Básica",
            "cliente": "Ana",
            "precio_original": 110.0,
            "descuento": 0,
            "precio_final": 110.0,
            "fecha": "2026-01-15 10:30:00",
        }
        stats = tienda.obtener_estadisticas()
        assert stats["total_muebles"] == 0
        assert stats["ventas_realizadas"] == 1
        assert stats["total_muebles_vendidos"] == 1
        assert stats["valor_total_ventas"] == 110.0

    def test_realizar_venta_cliente_por_defecto(self, tienda, silla_basica):
        tienda.agregar_mueble(silla_basica)
        assert tienda.realizar_venta(silla_basica)["cliente"] == "Cliente Anónimo"

    def test_realizar_venta_con_descuento(self, tienda, silla_basica, mesa_basica):
        tienda.agregar_mueble(silla_basica)
        tienda.agregar_mueble(mesa_basica)
        tienda.aplicar_descuento("sillas", 10)

        venta_silla = tienda.realizar_venta(silla_basica)
        venta_mesa = tienda.realizar_venta(mesa_basica)

        assert venta_silla["descuento"] == pytest.approx(10.0)
        assert venta_silla["precio_final"] == pytest.approx(99.0)
        assert venta_mesa["descuento"] == 0
        assert venta_mesa["precio_final"] == pytest.approx(104.8)

    def test_realizar_venta_mueble_fuera_de_inventario(self, tienda, silla_basica):
        assert tienda.realizar_venta(silla_basica) == {
            "error": "El mueble no está disponible en inventario"
        }

    def test_realizar_venta_sin_nombre_usa_el_tipo(self, tienda, silla_basica):
        tienda.agregar_mueble(silla_basica)
        silla_basica._nombre = ""
        assert tienda.realizar_venta(silla_basica)["mueble"] == "Silla"

    def test_realizar_venta_con_error_de_precio(self, tienda):
        mueble = mueble_con_fallo()
        tienda.agregar_mueble(mueble)

        resultado = tienda.realizar_venta(mueble)

        assert resultado == {"error": "Error al procesar la venta: falla"}
        assert tienda.obtener_estadisticas()["ventas_realizadas"] == 0


class TestEstadisticas:
    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas(self, tienda_con_muebles, comedor_completo, metodo):
        tienda_con_muebles.agregar_comedor(comedor_completo)
        tienda_con_muebles.aplicar_descuento("mesas", 15)

        stats = getattr(tienda_con_muebles, metodo)()

        assert stats["total_muebles"] == 3
        assert stats["total_comedores"] == 1
        assert stats["valor_inventario"] == pytest.approx(394.8)
        assert stats["tipos_muebles"] == {"Silla": 2, "Mesa": 1}
        assert stats["descuentos_activos"] == {"Mesa": 0.15}
        assert stats["total_muebles_vendidos"] == 0
        assert stats["valor_total_ventas"] == 0.0

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_ignoran_muebles_con_error_de_precio(self, tienda, silla_basica, metodo):
        tienda.agregar_mueble(silla_basica)
        tienda.agregar_mueble(mueble_con_fallo())
        stats = getattr(tienda, metodo)()
        assert stats["total_muebles"] == 2
        assert stats["valor_inventario"] == pytest.approx(110.0)

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_devuelven_valores_por_defecto_ante_error(self, tienda, metodo):
        tienda._inventario = None  # provoca un error interno
        stats = getattr(tienda, metodo)()
        assert stats["total_muebles"] == 0
        assert stats["valor_inventario"] == 0.0
        assert stats["tipos_muebles"] == {}

    def test_descuentos_activos_es_una_copia(self, tienda):
        tienda.aplicar_descuento("sillas", 10)
        tienda.obtener_estadisticas()["descuentos_activos"].clear()
        assert tienda.obtener_estadisticas()["descuentos_activos"] == {"Silla": 0.1}


class TestReporte:
    def test_reporte_inventario(self, tienda_con_muebles):
        tienda_con_muebles.aplicar_descuento("sillas", 10)

        reporte = tienda_con_muebles.generar_reporte_inventario()

        assert reporte.startswith("=== REPORTE DE INVENTARIO - Tienda de Prueba ===")
        assert "Total de muebles: 3" in reporte
        assert "Total de comedores: 0" in reporte
        assert "Valor total del inventario: $394.80" in reporte
        assert "- Silla: 2 unidades" in reporte
        assert "- Mesa: 1 unidades" in reporte
        assert "DESCUENTOS ACTIVOS:\n- Silla: 10.0%" in reporte

    def test_reporte_sin_descuentos(self, tienda_con_muebles):
        assert "DESCUENTOS ACTIVOS" not in tienda_con_muebles.generar_reporte_inventario()

    @pytest.mark.parametrize("retorno", [None, "no es un dict"])
    def test_reporte_tolera_estadisticas_invalidas(self, tienda, retorno):
        with patch.object(tienda, "obtener_estadisticas", return_value=retorno):
            reporte = tienda.generar_reporte_inventario()
        assert "Total de muebles: 0" in reporte
        assert "Valor total del inventario: $0.00" in reporte
