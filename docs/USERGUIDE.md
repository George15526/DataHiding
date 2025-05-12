# User Guide 使用手冊

## 如果想要玩玩看此專案，那你一定要看
### 需先下載的軟體/套件
* Python v3.13
* Git bash(有的話可直接使用git clone，更方便；若無，則需要將專案的Zip檔載下來使用)
* VSCode(或其他自己習慣的編譯器)

### 流程：
* Step 1 -- clone此專案:<br>
  * 使用 Git:<br>
    `git clone https://github.com/George15526/DataHiding.git`

  * 使用Zip檔(點選紅色圓圈處):
    <img src="https://github.com/user-attachments/assets/2c381ee8-2d15-4a5a-bb26-2a4869e1ed3b" height="35%" >
    
* Step 2 -- 利用編譯器打開專案並在terminal中輸入以下指令:
  * 安裝pipenv虛擬環境與相關套件(此指令會根據Pipfile來安裝相關依賴，且不影響電腦環境):<br>
    `pipenv install`

  * 安裝完成後，進入pipenv虛擬環境:<br>
    `pipenv shell`

  * 運行專案:<br>
    `py app.py`
  > 在運行前，要注意是否將`port 8001`空下來，否則會跑不了哦
  
* Step 3:
  最後，在瀏覽器中開啟 [http://127.0.0.1:8001/](http://127.0.0.1:8001/)，即可開始使用！

> 註: 加密完後，記得將加密完顯示的圖片，進行存檔，並記住剛才設定的P值(若無設定，則後續解密就不用填)<br>
      在解密時，輸入剛剛所設定的P值，並選擇其加密後的圖片，方可成功解密