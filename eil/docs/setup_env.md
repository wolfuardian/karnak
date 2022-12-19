如何使用 PyCharm 編寫 Maya 介面

所需環境：
1. 安裝 Maya 2017 以上的版本，具體版本對應請參閱：https://www.cnblogs.com/ibingshan/p/9764886.html
2. PyCharm 最新版本 2022.3，下載頁面：https://www.jetbrains.com/pycharm/
   1. 安裝 MayaCharm 外掛
      1. 到 `File`－`Settings`－`Plugins`
      2. 搜尋 `MayaCharm` 並安裝
      3. 完成之後，此時你的 `Run` 底下應該會多出三行 Maya 相關的指令
      <br>![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/run_py_with_maya.png)
   2. 開啟你的專案
   3. 設定你的 Python 編譯器
      1. 到 `File`－`Settings`－`Project`－`Python Interpreter`
      2. 點選 `Python Interpreter:` 下拉式選單
      <br>![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/python_interpreter_droplsit.png)
      2. 選擇 `ShowAll...`
      3. Interpreter path 選擇你的 Interpreter 位置 `C:\Program Files\Autodesk\Maya[版本]\bin\mayapy.exe`
      <br>![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/python_interpreter_path.png)


3. 測試你的第一個腳本，測試腳本可參閱：https://github.com/wolfuardian/karnak/tree/main/eil/docs/examples
   1. 開啟 Maya，打開 Script Editor
   2. 輸入以下程式碼並執行
      ```python
      import maya.cmds as cmds
      
      if not cmds.commandPort(":4434", query=True):
          cmds.commandPort(name=":4434")
      ```
   3. 回到 PyCharm 打開測試用腳本 `qt_dockable_example.py`
   4. 到 `Run`－`Execute document in Maya`
   5. 點擊並在 Maya 視窗中察看結果
   <br>![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/example_window.png)
   <br>![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/docking_window.png)
   <br>![image](https://raw.githubusercontent.com/wolfuardian/karnak/main/eil/docs/images/docked_window.png)