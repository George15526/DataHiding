# DataHiding

改良以直方圖位移技術為基礎之可逆式隱藏方法 <br>
Data Hiding program using by Histogram Shifting (no overhead information)<br>

### 主要畫面(藏密或解密，二擇一)
<img src="https://github.com/user-attachments/assets/b21de4d9-21f4-471d-aff7-cf83c12682ca" height="400" >

### 藏密畫面
* 顯示P值、嵌入後的圖片(皆轉成黑白圖，方便處理)與結果直方圖
  
  * 無指定P值，則預定為最高峰，並將藏密之字元長度記錄在 `/static/data/data.json` 中：
  <img src="https://github.com/user-attachments/assets/4b46a800-1f10-4eea-ab3e-53cec1795125" height="400" >

  * 指定P值為：
  <img src="https://github.com/user-attachments/assets/4b8c928b-f891-4959-8ec5-0003660ecc32" height="400" >


### 解密畫面
* 顯示解密值、還原後的圖片(黑白圖)與還原後的結果直方圖

  * 無指定P值，則預定為最高峰：
  <img src="https://github.com/user-attachments/assets/ad704f2d-f7bb-4459-8996-78d97bf82f1d" height="400" >

  * 指定P值為：
  <img src="https://github.com/user-attachments/assets/8e5fe3e5-3d95-446a-af98-6007a326803a" height="400" >
