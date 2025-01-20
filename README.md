# Pytest 新手村攻略 (〃'▽'〃)

歡迎來到 Pytest 的世界！這個教學專案會帶你從最基礎的測試寫法，一路玩到複雜的 LangGraph 測試！(ﾉ>ω<)ﾉ

## 目錄
1. [環境準備](#環境準備)
2. [基礎概念](#基礎概念)
3. [從加法開始](#從加法開始)
4. [進階到除法](#進階到除法)
5. [實戰 LangGraph](#實戰-langgraph)

## 環境準備 (⁎˃ᴗ˂⁎)

首先，我們需要安裝必要的套件：

```bash
pip install pytest
pip install pytest-asyncio  # 用於測試非同步函數
```

## 基礎概念 (｡◕‿◕｡)

Pytest 有幾個重要的概念：

1. **測試檔案命名**：
   - 檔案名稱必須是 `test_*.py` 或 `*_test.py`
   - 測試函式必須是 `test_` 開頭

2. **斷言（assert）**：
   - 用 `assert` 來檢查結果是否符合預期
   - 例如：`assert 1 + 1 == 2`

3. **測試Fixture**：
   - 用 `@pytest.fixture` 來準備測試環境
   - 可重複使用的測試資料或設定

## 從加法開始 (◕‿◕✿)

讓我們看看 `test_basic_add_func.py` 的範例：

### 基本測試
```python
def test_demo_add():
    assert demo_add(1, 2) == 3
```
這是最簡單的測試！只要確認 1+2 是不是等於 3 。

### 參數化測試
```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),      # 正數加法
    (0, 0, 0),      # 零的處理
    (-5, -7, -12),  # 負數加法
])
```
這樣就可以一次測試很多情況，超級方便的啦！ヽ(✿ﾟ▽ﾟ)ノ

## 進階到除法 (╯✧▽✧)╯

在 `test_basic_divide_func.py` 中，我們學習更多進階技巧：

### 例外處理測試
```python
def test_divide_by_zero():
    with pytest.raises(ValueError):
        demo_divide(1, 0)
```
這樣就可以測試「應該要出錯的情況」！

### 使用 Fixture
```python
@pytest.fixture
def calculator_values():
    return {
        "normal_numbers": [(10, 2), (8, 4)],
        "small_numbers": [(0.1, 0.2)]
    }
```
Fixture 就像是一個百寶箱，把常用的測試資料都放進去！(｡♥‿♥｡)

## 實戰 LangGraph ᕦ(ò_óˇ)ᕤ

最後來看看 `test_plan_execute.py`，這是比較進階的應用：

### 測試非同步函數
```python
@pytest.mark.asyncio
async def test_plan_step():
    # 測試程式碼
```
要記得加上 `@pytest.mark.asyncio` 才能測試 async 函數喔！

### 模擬真實環境
```python
@pytest.fixture
def tools():
    return [TavilySearchResults(max_results=3)]
```
測試 AI 相關功能時，我們需要模擬真實的工具和環境～

## 執行測試 (◍•ᴗ•◍)

執行單一測試檔案：
```bash
pytest tests/test_basic_add_func.py -v
```

執行所有測試：
```bash
pytest -v
```

加上 `-v` 可以看到更詳細的測試結果！

## 常見問題 (｡•́︿•̀｡)

1. **測試沒有被發現？**
   - 檢查檔名是否正確（test_*.py）
   - 檢查函式名稱是否以 test_ 開頭

2. **Fixture 無法使用？**
   - 確認 fixture 名稱是否正確
   - 檢查是否有正確 import pytest

3. **非同步測試失敗？**
   - 確認有安裝 pytest-asyncio
   - 檢查是否有加上 @pytest.mark.asyncio

## 進階技巧 (≧◡≦)

1. **測試覆蓋率報告**：
```bash
pytest --cov=src tests/
```

2. **平行執行測試**：
```bash
pytest -n auto
```

3. **選擇性執行測試**：
```bash
pytest -k "add"  # 執行名稱中含有 "add" 的測試
```

## 結語 (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧

記住，寫測試不是為了讓程式碼更複雜，而是為了讓我們更有信心！
希望這個教學讓你愛上寫測試～

如果有任何問題，歡迎發 Issue 討論！我們一起進步！(♡˙︶˙♡)

祝測試愉快！٩(◕‿◕｡)۶
