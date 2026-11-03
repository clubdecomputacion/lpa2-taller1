"""
Pruebas de la clase SofaCama (herencia múltiple de Sofa y Cama).
"""

import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from models.concretos.sofa import Sofa
from models.concretos.cama import Cama
from models.concretos.sofacama import SofaCama


class TestSofaCamaHerenciaMultiple:
    def test_es_sofa_y_cama(self, sofacama_basico):
        assert isinstance(sofacama_basico, Sofa)
        assert isinstance(sofacama_basico, Cama)
        assert isinstance(sofacama_basico, Asiento)
        assert isinstance(sofacama_basico, Mueble)

    def test_orden_de_resolucion_mro(self):
        assert SofaCama.__mro__[:5] == (SofaCama, Sofa, Asiento, Cama, Mueble)

    def test_calcular_precio_se_redefine(self):
        assert SofaCama.calcular_precio is not Sofa.calcular_precio
        assert SofaCama.calcular_precio is not Cama.calcular_precio


class TestSofaCamaConstruccion:
    def test_valores_por_defecto(self, sofacama_basico):
        assert sofacama_basico.capacidad_personas == 3
        assert sofacama_basico.tiene_respaldo is True
        assert sofacama_basico.material_tapizado == "tela"
        assert sofacama_basico.tiene_brazos is True
        assert sofacama_basico.tamaño == "matrimonial"
        assert sofacama_basico.tamaño_cama == "matrimonial"
        assert sofacama_basico.incluye_colchon is True
        assert sofacama_basico.mecanismo_conversion == "plegable"
        assert sofacama_basico.modo_actual == "sofa"


class TestSofaCamaPrecio:
    def test_precio_por_defecto(self, sofacama_basico):
        # Sofá: 1000 * 1.3 + 150 = 1450; cama: +300 (matrimonial) +250 (colchón)
        assert sofacama_basico.calcular_precio() == pytest.approx(2000.0)

    @pytest.mark.parametrize(
        "tamaño,extra",
        [("individual", 0), ("matrimonial", 300), ("queen", 500), ("king", 700)],
    )
    def test_extra_por_tamaño(self, tamaño, extra):
        sofacama = SofaCama("SC", "Tela", "Beige", 1000.0, tamaño_cama=tamaño, incluye_colchon=False)
        assert sofacama.calcular_precio() == pytest.approx(1450.0 + extra)

    @pytest.mark.parametrize(
        "mecanismo,extra",
        [("plegable", 0), ("extensible", 0), ("hidraulico", 150), ("electrico", 300)],
    )
    def test_extra_por_mecanismo(self, mecanismo, extra):
        sofacama = SofaCama("SC", "Tela", "Beige", 1000.0, mecanismo_conversion=mecanismo)
        assert sofacama.calcular_precio() == pytest.approx(2000.0 + extra)


class TestSofaCamaConversion:
    def test_convertir_a_cama(self, sofacama_basico):
        assert sofacama_basico.convertir_a_cama() == (
            "Sofá convertido a cama usando mecanismo plegable"
        )
        assert sofacama_basico.modo_actual == "cama"

    def test_convertir_a_cama_dos_veces(self, sofacama_basico):
        sofacama_basico.convertir_a_cama()
        assert sofacama_basico.convertir_a_cama() == "El sofá-cama ya está en modo cama"

    def test_convertir_a_sofa_estando_en_sofa(self, sofacama_basico):
        assert sofacama_basico.convertir_a_sofa() == "El sofá-cama ya está en modo sofá"

    def test_convertir_a_sofa_desde_cama(self, sofacama_basico):
        sofacama_basico.convertir_a_cama()
        assert sofacama_basico.convertir_a_sofa() == (
            "Cama convertida a sofá usando mecanismo plegable"
        )
        assert sofacama_basico.modo_actual == "sofa"


class TestSofaCamaCapacidadYDescripcion:
    def test_capacidad_total_matrimonial(self, sofacama_basico):
        assert sofacama_basico.obtener_capacidad_total() == {"como_sofa": 3, "como_cama": 2}

    def test_capacidad_total_individual(self):
        sofacama = SofaCama("SC", "Tela", "Beige", 1000.0, capacidad_personas=2, tamaño_cama="individual")
        assert sofacama.obtener_capacidad_total() == {"como_sofa": 2, "como_cama": 1}

    def test_descripcion(self, sofacama_basico):
        desc = sofacama_basico.obtener_descripcion()
        assert desc.startswith("Sofá-Cama: SofaCama Básico")
        assert "Capacidad: 3 personas, Respaldo: Sí, Tapizado: tela" in desc
        assert "Tamaño como cama: matrimonial" in desc
        assert "Incluye colchón: Sí" in desc
        assert "Mecanismo: plegable" in desc
        assert "Modo actual: sofa" in desc
        assert "Precio final: $2000.0" in desc

    def test_descripcion_sin_colchon(self):
        sofacama = SofaCama("SC", "Tela", "Beige", 1000.0, incluye_colchon=False)
        assert "Incluye colchón: No" in sofacama.obtener_descripcion()

    def test_str_muestra_el_modo(self, sofacama_basico):
        assert str(sofacama_basico) == "Sofá-cama SofaCama Básico (modo: sofa)"
        sofacama_basico.convertir_a_cama()
        assert str(sofacama_basico) == "Sofá-cama SofaCama Básico (modo: cama)"
