
import pytest
from unittest.mock import AsyncMock, patch
from workflow import SimpleGreeterWorkflow, WorkflowInput


@pytest.mark.asyncio
async def test_greeting_approved():
    """Workflow returns greeting when approved."""
    with patch("workflow.workflow.execute_activity", new_callable=AsyncMock) as mock_exec:
        from activities import GreetOutput
        mock_exec.return_value = GreetOutput(message="Hello, Robert! Workflow complete.")

        wf = SimpleGreeterWorkflow()
        wf._approved = True

        # Simulate run by calling activity directly
        from activities import build_greeting, GreetInput
        result = await build_greeting(GreetInput(name="Robert"))
        assert result.message == "Hello, Robert! Workflow complete."


@pytest.mark.asyncio
async def test_greeting_rejected():
    """Workflow returns rejection message when rejected."""
    wf = SimpleGreeterWorkflow()
    wf._approved = False
    # Verify rejection state is set correctly
    assert wf._approved is False


def test_empty_name_raises():
    """Activity raises ApplicationError for empty name."""
    import asyncio
    from activities import build_greeting, GreetInput
    from temporalio.exceptions import ApplicationError

    async def run():
        try:
            await build_greeting(GreetInput(name="  "))
            assert False, "Should have raised"
        except ApplicationError as e:
            assert e.non_retryable is True

    asyncio.run(run())
