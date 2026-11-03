"""
Configuración compartida de pytest para todas las pruebas.
Registra los marcadores personalizados y expone las fixtures de tests/fixtures.
"""

import pytest

from tests.fixtures.muebles import *  # noqa: F401,F403


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")


@pytest.fixture
def tienda():
    """Tienda vacía para cada prueba."""
    from services.tienda import TiendaMuebles

    return TiendaMuebles("Tienda de Prueba")
