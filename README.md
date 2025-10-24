🎉 WhatsApp Birthday Notifier by Elvri

Script otomatis untuk mengirim ucapan ulang tahun melalui WhatsApp Web menggunakan Python + Selenium.
Mendukung kirim pesan personal, grup, serta lampiran gambar.

⚙️ 1. Instalasi Awal
🐍 Install Python

Pastikan Python 3.10+ sudah terpasang.
Cek versi:

python --version

📦 Install Dependencies

Buka CMD / Terminal di folder yang sama dengan hbd.py, lalu jalankan:

pip install -r requirements.txt


Python akan otomatis mengunduh semua library yang dibutuhkan:

pandas
openpyxl
selenium
webdriver-manager
python-dateutil
colorama

📁 2. Konfigurasi File hbd.py

Buka file hbd.py dan sesuaikan bagian CONFIG di atas:

Variabel	Deskripsi
EXCEL_PATH	Lokasi file Excel berisi data ulang tahun (birthdays.xlsx)
HBD_MESSAGE_FILE	Lokasi template pesan personal (hbdmessage.txt)
GROUP_MESSAGE_FILE	Lokasi template pesan grup (messagegroup.txt)
USER_DATA_DIR	Lokasi penyimpanan sesi login browser
IMAGE_PATH	Lokasi gambar yang ingin dikirim (opsional, hanya untuk personal)
SEND_PERSONAL	True untuk kirim pesan ke masing-masing orang
SEND_TO_GROUP	True untuk kirim pesan ke grup WhatsApp
GROUP_ID	Kode grup WhatsApp (contoh: CBZnKzdPcW92qBvY6CM64Q)
![alt text](image.png)
HEADLESS	True untuk menjalankan browser tanpa tampilan (lihat penjelasan di bawah)
🧠 3. Tentang File Pendukung
🗓️ birthdays.xlsx

Berisi kolom berikut:

name	nik	birthdate	phone
John Doe	12345	1990-10-24	628123456789

Pastikan format tanggal (birthdate) valid dan kolom lengkap.

💌 hbdmessage.txt

Template untuk pesan pribadi.
Gunakan {name} sebagai placeholder untuk nama penerima.

Contoh:

Halo {name}, selamat ulang tahun! 🎉
Semoga panjang umur dan penuh berkat 🙏

👥 messagegroup.txt

Template untuk pesan grup.
Gunakan {names} sebagai placeholder daftar nama.

Contoh:

🎂 Halo semua! Hari ini ulang tahun {names}. 
Yuk kita ucapkan selamat dan doakan yang terbaik! 🥳

🚀 4. Cara Menjalankan

Buka CMD / Terminal di folder yang sama dengan hbd.py, lalu jalankan:

py .\hbd.py


Browser Chrome akan terbuka dan:

Jika belum login, akan muncul QR Code → scan dengan WhatsApp di HP.

Jika sudah ada sesi tersimpan di USER_DATA_DIR, langsung lanjut tanpa scan.

🕵️‍♂️ 5. Mode Headless (Tanpa Tampilan)

Kamu bisa menjalankan script tanpa membuka browser GUI — cocok untuk automation/scheduler server.

Set di config:

HEADLESS = True


⚠️ Peringatan penting:

Jalankan mode headless hanya jika kamu sudah login sebelumnya.

Jika belum ada sesi tersimpan, headless tidak bisa menampilkan QR Code untuk scan login.

Disarankan login dulu sekali dengan HEADLESS = False, agar sesi tersimpan di USER_DATA_DIR.

🗓️ 6. Menjalankan Otomatis Setiap Hari (Windows)

Buat file hbd.bat di folder yang sama:

@echo off
cd /d "D:\Projects\whatsapp-blast"
py hbd.py


Lalu pasang di Windows Task Scheduler:

Trigger: Daily

Time: 07:00 AM (misal)

Action: Run hbd.bat

✅ 7. Fitur Utama

🔁 Otomatis membaca data ulang tahun harian dari Excel.

💬 Kirim pesan personal dengan nama dinamis {name}.

👥 Kirim satu pesan ke grup dengan daftar nama {names}.

📎 Kirim gambar otomatis jika diaktifkan.

🧠 Menyimpan sesi login WhatsApp, jadi tidak perlu scan QR setiap hari.

⚡ Headless mode untuk automation server.

🧾 8. Contoh Output di CMD
🎉 WhatsApp Birthday Notifier by Elvri

📘 Reading Excel: D:\Projects\whatsapp-blast\birthdays.xlsx
✅ Found 2 birthdays today!
🎈 Sending to John Doe (628123456789)...
✅ Message sent to John Doe
📎 Image sent to John Doe
📢 Sending message to group via GROUP ID...
✅ Group message sent successfully!

Done in 0:01:12

🧰 9. Struktur Folder Disarankan
D:\Projects\whatsapp-blast\
│
├── hbd.py
├── requirements.txt
├── birthdays.xlsx
├── hbdmessage.txt
├── messagegroup.txt
├── chrome_user_data\
└── hbd.bat

⚡ Credit

Developed by Elvri — automation & planning expert ⚙️
Forward-thinking script for effortless WhatsApp greetings 🎂
