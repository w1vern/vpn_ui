import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from typing import Any, Dict, Generator, AsyncGenerator

import pytest_asyncio

from services.backend.services.server import ServerService
from services.backend.exceptions.s403 import NotServerEditorException
from services.backend.exceptions.s404 import ServerNotFoundException
from services.backend.schemas.server import (
    ServerSchema,
    CreateServerSchema,
    ServerToEditSchema,
)


@pytest_asyncio.fixture
def mock_repos() -> Dict[str, Any]:
    """Создаём моки для всех зависимостей ServerService."""
    return {
        "session": AsyncMock(),
        "ur": AsyncMock(),
        "sr": AsyncMock(),
        "psr": AsyncMock(),
        "user_schema": MagicMock(),
    }


@pytest_asyncio.fixture
def service(mock_repos: Dict[str, Any]) -> ServerService:
    """Инстанс сервиса с моками."""
    return ServerService(**mock_repos)


@pytest.mark.asyncio
async def test_all_returns_servers(service: ServerService, mock_repos: Dict[str, Any]) -> None:
    # Arrange
    fake_servers = [MagicMock(), MagicMock()]
    mock_repos["psr"].get_all.return_value = fake_servers

    # Act
    result: list[ServerSchema] = await service.all()

    # Assert
    assert isinstance(result, list)
    assert all(isinstance(s, ServerSchema) for s in result)
    mock_repos["psr"].get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_raises_if_not_editor(service: ServerService, mock_repos: Dict[str, Any]) -> None:
    # Arrange
    mock_repos["user_schema"].rights.is_server_editor = False
    server_to_create: CreateServerSchema = MagicMock(spec=CreateServerSchema)

    # Act / Assert
    with pytest.raises(NotServerEditorException):
        await service.create(server_to_create)


@pytest.mark.asyncio
async def test_create_calls_repositories(service: ServerService, mock_repos: Dict[str, Any]) -> None:
    # Arrange
    mock_repos["user_schema"].rights.is_server_editor = True
    server_to_create: CreateServerSchema = MagicMock(spec=CreateServerSchema)

    fake_server: MagicMock = MagicMock()
    mock_repos["sr"].create.return_value = fake_server

    # Act
    await service.create(server_to_create)

    # Assert
    mock_repos["sr"].create.assert_awaited_once()
    mock_repos["psr"].create.assert_awaited_once_with(
        server=fake_server,
        panel_port=server_to_create.panel_port,
        port_generator_port=server_to_create.port_generator_port,
        web_path=server_to_create.web_path,
        login=server_to_create.login,
        password=server_to_create.password,
    )


@pytest.mark.asyncio
async def test_edit_raises_if_not_editor(service: ServerService, mock_repos: Dict[str, Any]) -> None:
    # Arrange
    mock_repos["user_schema"].rights.is_server_editor = False

    # Act / Assert
    with pytest.raises(NotServerEditorException):
        await service.edit(uuid4(), MagicMock(spec=ServerToEditSchema))


@pytest.mark.asyncio
async def test_edit_raises_if_server_not_found(service: ServerService, mock_repos: Dict[str, Any]) -> None:
    # Arrange
    mock_repos["user_schema"].rights.is_server_editor = True
    mock_repos["sr"].get_by_id.return_value = None
    mock_repos["psr"].get_by_id.return_value = None

    # Act / Assert
    with pytest.raises(ServerNotFoundException):
        await service.edit(uuid4(), MagicMock(spec=ServerToEditSchema))


@pytest.mark.asyncio
async def test_edit_updates_fields(service: ServerService, mock_repos: Dict[str, Any]) -> None:
    # Arrange
    mock_repos["user_schema"].rights.is_server_editor = True

    fake_server: MagicMock = MagicMock()
    fake_pserver: MagicMock = MagicMock()
    mock_repos["sr"].get_by_id.return_value = fake_server
    mock_repos["psr"].get_by_id.return_value = fake_pserver

    server_to_edit: ServerToEditSchema = MagicMock(spec=ServerToEditSchema)
    server_to_edit.ip = "127.0.0.1"
    server_to_edit.country_code = "US"
    server_to_edit.display_name = "test-server"
    server_to_edit.starting_date = None
    server_to_edit.closing_date = None
    server_to_edit.is_available = True
    server_to_edit.login = "admin"
    server_to_edit.password = "secret"
    server_to_edit.panel_port = 8080
    server_to_edit.port_generator_port = 9090
    server_to_edit.web_path = "/srv"
    server_to_edit.description = "Test desc"

    # Act
    await service.edit(uuid4(), server_to_edit)

    # Assert — проверяем, что вызвались сеттеры
    mock_repos["sr"].set_ip.assert_awaited_once_with(fake_server, server_to_edit.ip)
    mock_repos["sr"].set_country_code.assert_awaited_once()
    mock_repos["sr"].set_display_name.assert_awaited_once()
    mock_repos["sr"].set_is_available.assert_awaited_once()
    mock_repos["sr"].set_description.assert_awaited_once()
    mock_repos["psr"].set_login.assert_awaited_once()
    mock_repos["psr"].set_password.assert_awaited_once()
    mock_repos["psr"].set_panel_port.assert_awaited_once()
    mock_repos["psr"].set_port_generator_port.assert_awaited_once()
    mock_repos["psr"].set_web_path.assert_awaited_once()
