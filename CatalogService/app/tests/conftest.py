import pytest
from unittest.mock import AsyncMock
from logic.services.catalog import BaseCatalogService
from logic.services.order import BaseOrderService
from logic.services.storage import BaseStorageService
from logic.commands.category import AddCategoryCommandHandler
from logic.commands.order import CreateOrderCommandHandler
from logic.commands.storage import AddStorageCommandHandler

# Мокируем сервисы, которые могут быть использованы в тестах
@pytest.fixture
def mock_catalog_service():
    """Фикстура для мокирования CatalogService"""
    mock_service = AsyncMock(spec=BaseCatalogService)
    return mock_service


@pytest.fixture
def mock_order_service():
    """Фикстура для мокирования OrderService"""
    mock_service = AsyncMock(spec=BaseOrderService)
    return mock_service


@pytest.fixture
def mock_storage_service():
    """Фикстура для мокирования StorageService"""
    mock_service = AsyncMock(spec=BaseStorageService)
    return mock_service


# Мокированные обработчики команд
@pytest.fixture
def add_category_command_handler(mock_catalog_service):
    """Фикстура для AddCategoryCommandHandler"""
    handler = AddCategoryCommandHandler(catalog_service=mock_catalog_service)
    return handler


@pytest.fixture
def create_order_command_handler(mock_order_service):
    """Фикстура для CreateOrderCommandHandler"""
    handler = CreateOrderCommandHandler(order_service=mock_order_service)
    return handler


@pytest.fixture
def add_storage_command_handler(mock_storage_service):
    """Фикстура для AddStorageCommandHandler"""
    handler = AddStorageCommandHandler(storage_service=mock_storage_service)
    return handler


# Пример фикстуры для команд, если нужно передать конкретные команды
@pytest.fixture
def add_category_command():
    """Фикстура для AddCategoryCommand"""
    return AddCategoryCommand(token="some-token", parent_category="", category_name="New Category")


@pytest.fixture
def create_order_command():
    """Фикстура для CreateOrderCommand"""
    return CreateOrderCommand(token="some-token")
