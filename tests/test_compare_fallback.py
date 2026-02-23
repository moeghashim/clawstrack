from backend.analysis import compare_projects


def test_compare_fallback_without_api_key_returns_explainable_scores() -> None:
    response = compare_projects(
        repositories=["https://github.com/a/b", "https://github.com/c/d"],
        criteria=["features", "security"],
        level="summary",
        openai_api_key=None,
    )

    assert response.confidence > 0
    assert len(response.scores) == 2
    assert all(item.rationale for item in response.scores)
