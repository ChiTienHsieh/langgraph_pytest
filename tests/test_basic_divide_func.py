import pytest
from src.basic_divide_func import demo_divide

# 示範4：除法的成功例子
def test_demo_divide():
    assert demo_divide(6, 2) == 3.0
    assert demo_divide(5, 2) == 2.5

# 示範5：測試例外處理
# 說明：當我們預期程式會拋出例外時，應該這樣測試
def test_divide_by_zero():
    # pytest.raises 是用來測試「預期會發生的錯誤」
    # match參數可以確認錯誤訊息是否符合預期
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        demo_divide(1, 0)

# 故意錯的話可以發現會泡出 ValueError: Cannot divide by zero
def test_divide_by_zera_no_error_handle():
    demo_divide(1, 0)


# 示範6：參數化測試的另一個例子
# 這次我們測試更多除法的情況
@pytest.mark.parametrize("a, b, expected", [
    (6, 2, 3.0),     # 整數除法
    (5, 2, 2.5),     # 有小數點的結果
    (-6, 2, -3.0),   # 負數處理
    (0, 5, 0.0),     # 零的處理
    (10, 0.5, 20.0)  # 除以小於1的數
])
def test_demo_divide_parametrize(a, b, expected):
    assert demo_divide(a, b) == expected

# 示範7：Fixture的使用
# 說明：Fixture是pytest中用來準備測試環境的特殊功能
# 像是這裡我們準備了一個計算機需要的各種數值
@pytest.fixture
def calculator_values():
    # 回傳一個字典，包含多種測試案例
    return {
        "normal_numbers": [(10, 2), (8, 4), (100, 10)],  # 一般數字
        "small_numbers": [(0.1, 0.2), (0.01, 0.00003)],      # 小數點
        "big_numbers": [(1000000, 2), (999999, 3), (1000000, 3)]       # 大數字
    }

# 示範8：如何使用Fixture
# 說明：在函數參數中使用Fixture的名稱，pytest就會自動把值傳入
def test_demo_divide_with_fixture(calculator_values):
    # 使用前面準備好的測試數據
    for a, b in calculator_values["normal_numbers"]:
        assert demo_divide(a, b) == a / b

# 示範9：處理浮點數精確度問題
# 說明：在處理小數點時，要特別注意精確度的問題
def test_small_numbers(calculator_values):
    for a, b in calculator_values["small_numbers"]:
        result = demo_divide(a, b)
        # 使用abs和閾值來比較浮點數
        assert abs(result - (a / b)) < 1e-10


# 示範10：測試大數字
def test_big_numbers(calculator_values):
    for a, b in calculator_values["big_numbers"]:
        assert demo_divide(a, b) == a / b
