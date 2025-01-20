import pytest  # 第一步：引入pytest套件
from src.basic_add_func import demo_add

# 示範1：最基本的pytest測試方法
# 解說：pytest會自動找到以"test_"開頭的函數來執行測試
def test_demo_add():
    # 使用assert關鍵字來驗證結果是否符合預期
    # assert的概念就像是：「我相信這個運算的結果應該要是...」
    assert demo_add(1, 2) == 3
    assert demo_add(-1, 1) == 0
    assert demo_add(0, 0) == 0
    assert demo_add(-1, -1) == -2
# 示範2：故意製造一個錯誤，讓大家看看測試失敗時會發生什麼事
    # 這行應該會失敗，因為1+1=2，不是3
    # assert demo_add(1, 1) == 3


# 示範3：參數化測試 (Parametrize)
# 說明：這是一個進階的測試方法，可以用同一個測試函數測試多種情況
# @pytest.mark.parametrize 是一個「裝飾器」(decorator)，用來定義測試參數
@pytest.mark.parametrize("a, b, expected", [
    # 格式是：(輸入1, 輸入2, 預期結果)
    (1, 2, 3),      # 測試案例1：正數相加
    (0, 0, 0),      # 測試案例2：零的處理
    (100, 200, 300),# 測試案例3：大數字
    (-5, -7, -12),  # 測試案例4：負數相加
    # (1, 1, 3)
])
def test_demo_add_parametrize(a, b, expected):
    # 這個函數會自動使用上面定義的所有參數組合來測試
    assert demo_add(a, b) == expected


