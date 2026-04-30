# Guideline v0.2.2

## 1. เริ่มต้น

```bash
./setup.sh
```
สิ่งที่จะเกิดขึ้นคือ

1. Database ถูก Migrate
1. Superuser ถูกสร้างขึ้น
1. Court User ถูกสร้างขึ้น
1. Group ถูกสร้างขึ้น
1. มีการสร้าง และ Assign Permission ให้อัตโนมัติ

## 2. สร้างฟอร์ม

### ระบบการสร้างฟอร์มคำร้องสามารถเลือกวิธีทำได้ 2 แบบ

### 2.1 ทำฟอร์มคำร้องบนหน้าที่รูปร่างคล้ายเอกสาร

การสร้างฟอร์มจะมีทั้งหมด 4 Steps.

Step 0: เลือกผู้ที่เป็นเจ้าของตัวจริงของคำขอดังกล่าว

Step 1: กรอกข้อมูลแบบฟอร์มคำขอ (Reqform)

Step 2: กรอกข้อมูลหมาย (Warrant)

Step 3: ตรวจสอบความถูกต้อง

หากผู้ใช้ได้ทำ Step 1 หรือ Step 2 สำเร็จแล้ว ข้อมูลจะถูกเก็บไว้ใน Django Session ซึ่งจะหายไปก็ต่อเมื่อ Step 3 สำเร็จ

เมื่อกดยืนยันจะถือว่าสำเร็จการสร้างแบบฟอร์ม โดยจะมีการสร้าง reqno ที่เป็นการผสมกันระหว่าง req_case_type_id, reqform_number, และ req_year, ซึ่งไม่สามารถซ้ำกันได้

### 2.2 สร้างแบบฟอร์มจากแบบร่างคำร้อง (Draft)

การสร้างฟอร์มจะต้องสร้าง `FormDraftContainer` ซึ่งจะเก็บข้อมูลของ Reqform และ Warrant

ขั้นตอนจะคล้ายกับ 2.1 โดยเมื่อเสร็จทุกอย่างแล้ว ต้องกดปุ่มเพื่อสร้าง `FormAwaitingApproval` จากข้อมูลทั้งหมดที่เก็บไว้ข้างใน

---

ไม่ว่าจะแบบไหนก็ตาม**

การสร้างแบบฟอร์มที่สำเร็จ จะสร้าง Object ดังนี้:

- `FormAwaitingApproval` โดยเก็บ ReqformDataModel ไว้แบบ One-to-One
- `ReqformDataModel` เป็นแบบฟอร์มที่เก็บ WarrantDataModel แบบ Many-to-Many
- `WarrantDataModel` 

**แบบที่ 2.1 ในขณะนี้ จะสามารถใส่และสร้าง WarrantDataModel ได้เพียงแค่ 1 ฉบับเท่านั้น แต่ 2.2 สามารถสร้างได้หลายฉบับพร้อมกัน


## 3. รับรองฟอร์มและส่ง

การรับรองแบบฟอร์มจะทำการสร้าง Object เพิ่ม ดังนี้

- `VisualReqformData` ดูสถานะ Reqform
- `VisualWarrantData` ดูสถานะ Warrant

และจะทำการส่ง API ทันที หากการตั้งค่าเปิดเอาไว้


## 4. การให้ศาลแก้ไขสถานะ

ศาลจะสามารถส่ง API เข้ามาที่ Directory ดังกล่าว เพื่อเปลี่ยนค่าได้

```
VisualReqformData
{{ HOST }}/api/v1/update-status/reqwarrant/
```

```
VisualWarrantData
{{ HOST }}/api/v1/update-status/warrant/
```

โดยจะใช้ข้อมูลบางส่วนที่ถูกส่งมาเป็น Key ในการหา Reqform ที่ต้องการ ซึ่งจะทำให้เจอ Warrant ที่ต้องการด้วย

ข้อมูลส่วนที่เหลือจะถูกนำไปใส่และ Update ข้อมูลในฐานข้อมูล

ศาลจะไม่สามารถเข้าถึง API ได้ หากไม่มีการเพิ่ม JWT (JSON Web Token) ไว้ที่ Header

`Authorization: Bearer {{ JWT_TOKEN }}
`

โดยสามารถขอ JWT ได้จาก Directory ดังกล่าว ด้วยการส่ง POST Request

```
{{ HOST }}/api/v1/authenticate/

{
    username: XXX,
    password: YYY,   
}
```
JWT ดังกล่าวควรที่ออกได้ก็ต่อเมื่อเป็น User สำหรับการใช้ API เท่านั้น โดยในขณะนี้ได้ตั้งไว้ให้ User ที่มี Permission Edit ReqformSubmitted เท่านั้น และต้องไม่ใช่ Superuser

## 5. การส่งสถานะของ Warrant กลับไปให้ศาล

เมื่อได้ Warrant แล้ว จะสามารถส่งข้อมูลว่าได้มีการใช้หมายได้แล้วหรือไม่ให้กับศาลได้

(Work in Progress) > Need more information on how woa_no works and how sending works.