from flaskr import create_app



# 初期値
DATABASE = "database.db"

def test_create_app():
    app = create_app()

    # 期待値の確認
    assert app is not None
    assert app.config["DATABASE"] == DATABASE
    assert "main" in app.blueprints