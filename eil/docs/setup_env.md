如何使用 PyCharm 編寫 Maya 介面

所需環境：
1. 安裝 Maya 2017 以上的版本，具體版本對應請參閱：https://www.cnblogs.com/ibingshan/p/9764886.html
2. PyCharm 最新版本 2022.3，下載頁面：https://www.jetbrains.com/pycharm/
   1. 安裝 MayaCharm 外掛
      1. `File`－`Settings`－`Plugins`
      2. 搜尋 MayaCharm 並安裝 
   2. 開啟你的專案
   3. 設定你的 Python 編譯器
      1. `File`－`Settings`－`Project`－`Python Interpreter`
      2. 點選 `Python Interpreter:` 下拉式選單
      ![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/python_interpreter_droplsit.png)
      2. 選擇 `ShowAll...`
      3. Interpreter path 選擇你的 Interpreter 位置 `C:\Program Files\Autodesk\Maya[版本]\bin\mayapy.exe`
      ![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/python_interpreter_path.png)


3. 測試你的第一個腳本，測試腳本可參閱：https://github.com/wolfuardian/karnak/tree/main/eil/docs/examples
   1. 