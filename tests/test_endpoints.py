def test_get_word_sets(client):
    # データが正しく取得できるか確認
    response = client.get("/word_sets/?date=2024-10-14")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["word1"] == "apple"


def test_get_available_dates(client):
    # 日付のリストが正しく返されるか確認
    response = client.get("/word_sets/dates/")
    assert response.status_code == 200
    assert "available_dates" in response.json()
