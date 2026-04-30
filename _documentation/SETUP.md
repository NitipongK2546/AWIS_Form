## 1. เริ่มต้น

สามารถเริ่มจาก 0 ได้ผ่านคำสั่ง

```bash
./full_setup_docker.sh
```

ซึ่งจะสร้าง Docker และรัน

```bash
./setup.sh
```
โดยสิ่งที่จะเกิดขึ้นคือ

1. Database ถูก Migrate
1. Superuser ถูกสร้างขึ้น
1. Court User ถูกสร้างขึ้น
1. Group ถูกสร้างขึ้น
1. มีการสร้าง และ Assign Permission ให้อัตโนมัติ