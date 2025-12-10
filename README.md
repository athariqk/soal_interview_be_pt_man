# Soal Interview Backend Programmer PT MAN

Sudah mengimplementasikan 4 soal yang total berjumlah 100 point.

## Panduan

Dikembangkan menggunakan Python dan FastAPI agar dapat selesai dalam waktu singkat dan mudah untuk dicek.

Untuk menjalankan server, dapat menggunakan command ini di console:
```
fastapi run entrypoint.py
```

Lalu server dapat diakses melalui URL:
```
http://localhost:8000/
```

Daftar API dapat dilihat melalui Swagger UI yang berjalan di:
```
http://localhost:8000/docs#/
```

## Teknis

Menggunakan SQLite untuk menyimpan data user dan schedule.

Table `user` berupa tabel 2 kolom utama: `name` dan `start_date`. `start_date` adalah string dengan format penanggalan ISO (Y-m-d).

Table schedule berupa tabel 3 kolom utama: `user_id (int)`, `shift (int)` dan `day (int)`. Kegunaan kolom `day` adalah sebagai penanda tanggal. Nilainya inkremental, tidak boleh konflik dan dapat melebihi 6 (dimulai dari 0) yang dimana artinya jadwal shift terkait memiliki pola lebih dari satu minggu. Kemudian kolom `day` ini di-interpretasikan secara dinamis dalam bussiness logic hingga menjadi sebuah tanggal di kalender gregorius dan menghasilkan pola shift yang berulang (siklus) berdasarkan `start_date` dari seorang `user`. Kolom `shift` adalah sebuah enum biasa.

Contoh data dalam tabel `schedule`:
| id | user_id | shift | day |
|:--:|:-------:|:-----:|:---:|
| 1	 |    1	   |   2	| 0  |
| 2	 |    1	   |   2	| 1  |
| 3	 |    1	   |   4	| 2  |
| 4	 |    1	   |   4	| 3  |
| 5	 |    1	   |   3	| 4  |
| 6	 |    1	   |   3	| 5  |
| 7	 |    1	   |   1	| 6  |
| 8	 |    2	   |   4	| 0  |
| 9	 |    2	   |   4	| 1  |
| 10 |	  2    |   3    | 2  |
| 11 |	  2    |   3    | 3  |
| 12 |	  2    |   1    | 4  |
| 13 |	  2    |   2    | 5  |
| 14 |	  2    |   4    | 6  |
| 15 |	  3    |   3    | 0  |
| 16 |	  3    |   3    | 1  |
| 17 |	  3    |   2    | 2  |
| 18 |	  3    |   1    | 3  |
| 19 |	  3    |   2    | 4  |

File penting: `service\schedule_service.py`

Pengorganisasian kode terinspirasi dari framework yang diterapkan Laravel.
