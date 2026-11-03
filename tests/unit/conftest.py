"""
Fixtures compartidas por las pruebas unitarias.
Incluye subclases mínimas para poder instanciar las clases abstractas.
"""

import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from models.categorias.almacenamiento import Almacenamiento
from models.categorias.superficies import Superficie


class MuebleConcreto(Mueble):
    def calcular_precio(self) -> float:
        return self.precio_base

    def obtener_descripcion(self) -> str:
        return f"Mueble concreto: {self.nombre}"


class AsientoConcreto(Asiento):
    def calcular_precio(self) -> float:
        return round(self.precio_base * self.calcular_factor_comodidad(), 2)

    def obtener_descripcion(self) -> str:
        return self.obtener_info_asiento()


class AlmacenamientoConcreto(Almacenamiento):
    def calcular_precio(self) -> float:
        return round(self.precio_base * self.calcular_factor_almacenamiento(), 2)

    def obtener_descripcion(self) -> str:
        return self.obtener_info_almacenamiento()


class SuperficieConcreta(Superficie):
    def calcular_precio(self) -> float:
        return round(self.precio_base * self.calcular_factor_tamaño(), 2)

    def obtener_descripcion(self) -> str:
        return self.obtener_info_superficie()


@pytest.fixture
def mueble():
    return MuebleConcreto("Mueble Prueba", "Madera", "Café", 100.0)


@pytest.fixture
def asiento():
    """Asiento para 3 personas, con respaldo y tapizado de cuero."""
    return AsientoConcreto("Asiento Prueba", "Madera", "Negro", 100.0, 3, True, "cuero")


@pytest.fixture
def almacenamiento():
    """Almacenamiento con 3 compartimentos y 200 litros."""
    return AlmacenamientoConcreto("Almacén Prueba", "Madera", "Blanco", 100.0, 3, 200)


@pytest.fixture
def superficie():
    """Superficie de 100x100x75 cm (área 10000 cm²)."""
    return SuperficieConcreta("Superficie Prueba", "Vidrio", "Negro", 100.0, 100.0, 100.0, 75.0)
