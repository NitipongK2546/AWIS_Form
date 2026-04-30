## 1. เริ่มต้น

สามารถเริ่มจาก 0 ได้ผ่านคำสั่ง

```bash
./full_setup_docker.sh
```

โดยข้างในคือ

```bash
docker compose up -d --build

# รอจนกว่า Database จะเริ่มทำงานเต็มตัว 
# แล้วจึงจะไปขั้นต่อไป
# echo "Database Server is up" สามารถเปลี่ยนเป็นคำสั่งก็ได้
./_scripts/wait-for-it.sh localhost:3306 -- echo "Database Server is up."

# รัน setup.sh ใน Container ที่มี Server อยู่
docker exec awis_server ./setup.sh
```

โดยสิ่งที่จะเกิดขึ้นคือ

1. Database ถูก Migrate
1. Superuser ถูกสร้างขึ้น
1. Court User ถูกสร้างขึ้น
1. Group ถูกสร้างขึ้น
1. มีการสร้าง และ Assign Permission ให้อัตโนมัติ