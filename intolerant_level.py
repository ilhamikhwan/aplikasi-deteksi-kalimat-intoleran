import streamlit as st
import pandas as pd
import re
# Halaman kalkulator Level Intoleransi dan Intoleransi Umum

def render():
    st.header("Intolerant Level Calculator")
    st.write(
        "Gunakan kalkulator ini untuk menghitung skor Level Intoleransi per level, serta menghitung skor Intoleransi Umum berdasarkan input manual Anda."
    )
    st.markdown("---")
    
    
    # 1 hitung jumlah kata intoleransi per akun
    st.subheader("1. 📂 Hitung Jumlah Kemunculan Kata Intoleransi Setiap Level")
    upload_file = st.file_uploader("Unggah file CSV yang berisi kolom teks:", type=["csv"])
    corpus = {
    1: [
        "Berdebat", "Berbeda", "Cemburu", "Geram", "Iri", "Jengkel",
        "Keliru", "Kontra", "Kontradiksi", "Kurang jelas", "Kurang kuat",
        "Kurang masuk akal", "Kurang sesuai", "Mengeluh", "Ragu", "Salah",
        "Tak Setuju", "Tidak adil", "Tidak aplikatif", "Tidak bermanfaat",
        "Tidak berdasarkan bukti", "Tidak berdasarkan fakta", "Tidak bernilai",
        "Tidak berbobot", "Tidak berdasar", "Tidak berdaya guna",
        "Tidak berfaedah", "Tidak berisi", "Tidak berkualitas",
        "Tidak bersahabat", "Tidak bernilai tambah", "Tidak bisa dipercaya",
        "Tidak cerdas", "Tidak cocok", "Tidak efektif", "Tidak efisien",
        "Tidak futuristik", "Tidak informatif", "Tidak inklusif",
        "Tidak inovatif", "Tidak jujur", "Tidak kompatibel",
        "Tidak komunikatif", "Tidak konkret", "Tidak konsisten",
        "Tidak koheren", "Tidak kreatif", "Tidak logis", "Tidak masuk akal",
        "Tidak membantu", "Tidak mendalam", "Tidak mendidik",
        "Tidak mendukung", "Tidak mengena", "Tidak menginspirasi",
        "Tidak menarik", "Tidak memadai", "Tidak memiliki arah",
        "Tidak memiliki nilai tambah", "Tidak menyeluruh",
        "Tidak menyentuh", "Tidak nyambung", "Tidak obyektif",
        "Tidak original", "Tidak pas", "Tidak paham", "Tidak penting",
        "Tidak pragmatis", "Tidak produktif", "Tidak profesional",
        "Tidak progresif", "Tidak ramah", "Tidak ramah lingkungan",
        "Tidak rasional", "Tidak relevan", "Tidak responsif",
        "Tidak seimbang", "Tidak sesuai", "Tidak serasi", "Tidak signifikan",
        "Tidak sinkron", "Tidak solid", "Tidak sempurna", "Tidak sepadan",
        "Tidak sependapat", "Tidak sejalan", "Tidak sepakat", "Tidak stabil",
        "Tidak substantif", "Tidak substansial", "Tidak toleran",
        "Tidak universal", "Tidak visioner", "Tidak yakin", "Tidak berempati",
        "Tidak berbasis fakta", "Tidak akomodatif"
    ],
    2: [
        "Bobrok", "Bodoh", "Buruk", "Curang", "Dangkal", "Degradasi",
        "Dengki", "Egois", "Hina", "Iri hati", "Inkompeten", "Kurang Ajar",
        "Lemah", "Licik", "Malas", "Manipulatif", "Menipu", "Menyesatkan",
        "Munafik", "Nyinyir", "Omong kosong", "Omon-omon", "Orang Bodoh",
        "Orang Gila", "Pecundang", "Pelupa", "Pemalas", "Pembuat onar",
        "Pembohong", "Pendendam", "Penakut", "Penipu", "Picik", "Provokatif",
        "Serakah", "Sok berkuasa", "Sok penting", "Sok perfeksionis",
        "Sok pintar", "Sok suci", "Sok tahu", "Sombong", "Tidak ada kontribusi",
        "Tidak berbudi", "Tidak berdasar", "Tidak bertanggung jawab",
        "Tidak bijaksana", "Tidak bisa berkompromi", "Tidak cerdas",
        "Tidak kompeten", "Tidak konstruktif", "Tidak kritis", "Tidak logis",
        "Tidak manusiawi", "Tidak mau belajar", "Tidak mau memahami sudut pandang",
        "Tidak membangun", "Tidak mencintai damai", "Tidak menghargai",
        "Tidak menghargai waktu", "Tidak menghormati", "Tidak punya arah",
        "Tidak punya etika", "Tidak punya hati nurani", "Tidak punya malu",
        "Tidak punya prinsip", "Tidak punya tujuan", "Tukang fitnah",
        "Tukang nyinyir", "Tukang ribut", "Tukang tipu"
    ],
    3: [
        "Bahaya", "Bermuka dua", "Bohong", "Busuk", "Dogmatis", "Fanatik",
        "Hoaks", "Hoax", "Kebohongan", "Kepalsuan", "Komplotan",
        "Melawan", "Mengidoktrinasikan", "Menjijikkan", "Meremehkan",
        "Palsu", "Pemutarbalikan", "Penyesat", "Radikal", "Manipulator",
        "mafia", "bangsat", "gorong", "bajingan", "miskin", "ternakan",
        "biang", "rakus", "terkorup", "jongos", "dungu", "pencitraan"
    ],
    4: [
        "Anarki", "Cina", "Diskriminasi", "Ekstrimis", "Genosida", "Kafir",
        "Membunuh", "Musuh", "Pembunuh", "Pemusnahan", "Penghancur",
        "Penyesat", "Rasis", "Teroris", "Tidak berharga", "Pembakar",
        "Pemecah bangsa", "Pemimpin zalim", "Penakluk", "Penanam kebencian",
        "Penebar fitnah", "Penekan", "Penegak kebrutalan", "Pengadu domba",
        "Pengambil paksa", "Pengancam", "Pengendali kekerasan",
        "Pengganda konflik", "Penggerak kekerasan", "Penggerak kezaliman",
        "Penggerak separatis", "Pengguling kekuasaan", "Penghasut",
        "pengkhianat", "Penghancur budaya", "Penghancur kehidupan",
        "Penghancur moral", "Penghancur persatuan", "Penghancur sistem",
        "Penghina", "Pengintimidasi", "Penikmat penderitaan", "Penindas",
        "Penindas sistemik", "Penipuan besar", "Penista agama",
        "Penista budaya", "Penjahat besar", "Penjahat lingkungan",
        "Penjahat perang", "Penjaga diskriminasi", "Penjaga kasta",
        "Penjaga ketidakadilan", "Penjaga tirani", "Penjual isu konflik",
        "Penyalah kebencian", "Penyangkal hak", "Penyebar ajaran kebencian",
        "Penyebar ancaman", "Penyebar diskriminasi", "Penyebar hoax",
        "Penyebar kebencian", "Penyebar ketakutan", "Penyebar konflik",
        "Penyebar narasi negatif", "Penyebar propaganda", "Penyebar teror",
        "Penyiksa", "Penyulut kemarahan", "Penyulut pelanggaran",
        "Penyulut perpecahan", "Penyulut perang", "Penyerang HAM",
        "Penyerang minoritas", "Pelaku anarki", "Pelaku diskriminasi",
        "Pelaku ekstrimisme", "Pelaku intoleransi", "Pelaku kekerasan",
        "Pelaku kejahatan manusia", "Pelaku radikalisme", "Pemusnahan",
        "Perampas", "Perusak", "Perusak budaya", "Perusak hubungan",
        "Perusak sistem", "Provokator", "oligarki", "tangkap", "gantung",
        "rezim", "mati", "ganyang", "koruptor", "pecat", "makzulkan",
        "hancurkan", "penjarakan", "Lengserkan", "Penjajah", "Bubarkan",
        "Hanguskan", "Tumbangkan", "Benamkan", "Singkirkan", "Usir"
    ]
    }
    def clean_text(text):
        if pd.isnull(text):
            return ""
        text = re.sub(r"@\w+|#\w+|http\S+|www\S+", " ", text)
        text = re.sub(r"[^a-zA-Z\s]", " ", text).lower()
        text = re.sub(r"\s+", " ", text).strip()
        return text

    if upload_file is not None:
        df = pd.read_csv(upload_file)

        if 'full_text' not in df.columns:
            st.error("Kolom 'full_text' tidak ditemukan dalam file CSV.")
            return

        # Preprocessing teks
        df['cleaned_text'] = df['full_text'].apply(clean_text)

        # Hitung kemunculan kata per level
        results = []
        for lvl, words in corpus.items():
            found_words = set()
            total_count = 0
            pattern = r'\b(?:' + '|'.join(re.escape(w.lower()) for w in words) + r')\b'
            
            for text in df['cleaned_text'].dropna():
                matches = re.findall(pattern, text.lower())
                total_count += len(matches)
                found_words.update(matches)

            results.append({
                'level': lvl,
                'count': total_count,
                'word': ', '.join(sorted(found_words))
            })

        df_summary = pd.DataFrame(results).sort_values('level')
        st.dataframe(df_summary, use_container_width=True)

    else:
        st.info("Silakan unggah file CSV terlebih dahulu.")
    
    st.markdown("---")
    st.markdown(" ")

    # 2. Kalkulator Level Intoleransi
    st.subheader("2. Hitung Intoleransi Kata Per Level")
    sum_kata = st.number_input(
        "Masukkan ∑Kata (jumlah kata yang cocok):", min_value=0.0, format="%.2f"
    )
    sum_post_kata = st.number_input(
        "Masukkan ∑Post-Kata (jumlah post yang mengandung kata):", min_value=0.0, format="%.2f"
    )
    sum_post = st.number_input(
        "Masukkan ∑Post (jumlah seluruh post):", min_value=1.0, format="%.2f"
    )

    if st.button("Hitung Level Intoleransi"):
        if sum_post_kata == 0 or sum_post == 0:
            st.error("∑Post-Kata dan ∑Post harus lebih besar dari 0.")
        else:
            L_i = (sum_kata / sum_post_kata) * (sum_post_kata / sum_post) * 10
            st.write(f"**Skor Level Intoleransi:** {L_i:.2f}")

    st.markdown("---")
    st.markdown(" ")

    # 3. Kalkulator Intoleransi Umum
    st.subheader("3. Hitung Intoleransi Umum")
    st.write("Masukkan skor Level Intoleransi yang sudah dihitung untuk setiap level:")
    L1 = st.number_input("Skor Level 1:", min_value=0.0, format="%.2f", key="L1")
    L2 = st.number_input("Skor Level 2:", min_value=0.0, format="%.2f", key="L2")
    L3 = st.number_input("Skor Level 3:", min_value=0.0, format="%.2f", key="L3")
    L4 = st.number_input("Skor Level 4:", min_value=0.0, format="%.2f", key="L4")

    if st.button("Hitung Intoleransi Umum"):
        intoleransi_umum = L1 * 1 + L2 * 2 + L3 * 3 + L4 * 4
        st.write(f"**Skor Intoleransi Umum:** {intoleransi_umum:.2f}")

        # Kategori
        if intoleransi_umum <= 10:
            kategori = "Normal (0% - 10%)"
        elif intoleransi_umum <= 30:
            kategori = "Ringan (10,01% - 30%)"
        elif intoleransi_umum <= 60:
            kategori = "Sedang (30,01% - 60%)"
        else:
            kategori = "Tinggi (> 60%)"
        st.write(f"**Kategori:** {kategori}")