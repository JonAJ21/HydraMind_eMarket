import pytest
from unittest.mock import AsyncMock
from logic.commands.category import AddCategoryCommand, AddCategoryCommandHandler
from domain.entities.category import Category

@pytest.mark.asyncio
async def test_add_category_command_handler():
    mock_catalog_service = AsyncMock()
    mock_catalog_service.add_category.return_value = Category(
        oid="1", category_name="New Category", parent_category=""
    )
    
    command = AddCategoryCommand(token="some-token", parent_category="", category_name="New Category")
    
    handler = AddCategoryCommandHandler(catalog_service=mock_catalog_service)
    
    result = await handler.handle(command)
    
    mock_catalog_service.add_category.assert_awaited_once_with("some-token", "", "New Category")
    assert isinstance(result, Category)
    assert result.category_name == "New Category"
    assert result.parent_category == ""
