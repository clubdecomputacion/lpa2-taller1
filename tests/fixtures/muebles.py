"""
Datos de prueba reutilizables: fixtures con muebles ya construidos.
"""

import pytest

from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.sofa import Sofa
from models.concretos.cama import Cama
from models.concretos.sofacama import SofaCama
from models.composicion.comedor import Comedor


@pytest.fixture
def silla_basica():
    """Silla con respaldo y sin tapizado: precio final 110.0."""
    return Silla("Silla Básica", "Madera", "Café", 100.0)


@pytest.fixture
def silla_oficina():
    """Silla con cuero, altura regulable y ruedas: precio final 180.0."""
    return Silla(
        "Silla Oficina",
        "Metal",
        "Negro",
        100.0,
        tiene_respaldo=True,
        material_tapizado="cuero",
        altura_regulable=True,
        tiene_ruedas=True,
    )


@pytest.fixture
def mesa_basica():
    """Mesa rectangular 120x80 para 4 personas: precio final 104.8."""
    return Mesa("Mesa Básica", "Roble", "Natural", 100.0)


@pytest.fixture
def sofa_basico():
    """Sofá de 3 personas con brazos: precio final 270.0."""
    return Sofa("Sofá Básico", "Tela", "Gris", 100.0)


@pytest.fixture
def cama_basica():
    """Cama individual sin extras: precio final 500.0."""
    return Cama("Cama Básica", "Madera", "Blanco", 500.0)


@pytest.fixture
def sofacama_basico():
    """Sofá-cama con valores por defecto: precio final 2000.0."""
    return SofaCama("SofaCama Básico", "Tela", "Beige", 1000.0)


@pytest.fixture
def sillas_comedor():
    """Cuatro sillas con tapizado de tela: 120.0 cada una."""
    return [
        Silla(f"Silla Comedor {i}", "Madera", "Café", 100.0, material_tapizado="tela")
        for i in range(1, 5)
    ]


@pytest.fixture
def comedor_completo(mesa_basica, sillas_comedor):
    """Comedor con mesa para 4 y 4 sillas (aplica descuento del 5%)."""
    return Comedor("Familiar", mesa_basica, sillas_comedor)
