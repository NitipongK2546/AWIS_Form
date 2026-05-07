# API v0.2.3.1-fix-01

## 1. API ของภายนอก 

### 1.1 รายละเอียด

ศาลจะสามารถส่ง API เข้ามาที่ Directory ดังกล่าว เพื่อเปลี่ยนค่าได้

```
VisualReqformData
{{ HOST }}/api/v1/requests/<str:req_no_plaintiff>/
```

```
VisualWarrantData
{{ HOST }}/api/v1/warrant/<str:woa_refno>/
```

โดยจะใช้ข้อมูลบางส่วนที่ถูกส่งมาเป็น Key ในการหา Reqform ที่ต้องการ ซึ่งจะทำให้เจอ Warrant ที่ต้องการด้วย

ข้อมูลส่วนที่เหลือจะถูกนำไปใส่และ Update ข้อมูลในฐานข้อมูล

ศาลจะไม่สามารถเข้าถึง API ได้ หากไม่มีการเพิ่ม JWT (JSON Web Token) ไว้ที่ Header

`Authorization: Bearer {{ JWT_TOKEN }}
`

โดยสามารถขอ JWT ได้จาก URL ดังกล่าว ด้วยการส่ง POST Request

```
{{ HOST }}/api/v1/authenticate/

{
    username: XXX,
    password: YYY,   
}
```
JWT ดังกล่าวควรที่ออกได้ก็ต่อเมื่อเป็น User สำหรับการใช้ API เท่านั้น โดยในขณะนี้ได้ตั้งไว้ให้ User ที่มี Permission Edit ReqformSubmitted เท่านั้น และต้องไม่ใช่ Superuser

### 1.2 เพิ่มเติม

หากต้องการสร้าง API ตัวใหม่ สามารถสร้าง Folder เพิ่มลงไป เช่น v1.1 และเพิ่ม urls.py ของตัวเอง พร้อมกับแก้ไข urls.py ของ /api ด้วย

Reverse url สามารถเข้าถึง API ได้โดย "api:v1.1:authenticate" เป้นต้น

## 2. API ภายใน (internal)

เป็น API สำหรับให้ User บน Browser ใช้ Javascript ส่งมาขอข้อมูลได้

ใช้เพื่อปกปิด API ที่ส่งให้ API Server ตัวจริง และถ้าข้อมูลมีขนาดมากเกินไป ให้ใช้ช่องทางนี้ส่งข้อมูลเพื่อลดเวลาในการโหลดของเว็บไซต์ได้

ตัวอย่างที่ใช้เช่น Sub_district ที่มีจำนวนมากที่ไม่สามารถเลือกได้ แต่ถูกโหลดหมดทีเดียว

## Extra: /_request_utils

เก็บ Function การเชื่อมต่อ API เข้า Server อื่น ๆ ไว้

หากการส่ง API มีปัญหา ให้ลองแก้ไฟล์ใน Directory นี้