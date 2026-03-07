import streamlit as st
import pandas as pd
import pickle
import re
import nltk
from transformers import BertTokenizer
from nltk.corpus import stopwords
# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load vectorizer dan model
with open('models/svm_indobert_tokenizer/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('models/svm_indobert_tokenizer/svm_indobert_sigmoid_kernel.pkl', 'rb') as f:
    model = pickle.load(f)

# Normalisasi teks
def normalize_text(text, slang_dict=None):
    if slang_dict:
        for slang, formal in slang_dict.items():
            text = re.sub(rf"\b{slang}\b", formal, text, flags=re.IGNORECASE)
    return text


slang_dictionary = {
    'aja':'saja', 'bhw':'bahwa', 'byk':'banyak', 'bnyk':'banyak', 
    'biar':'agar', 'bu':'ibu', 'dpt':'dapat', 'dr':'dari', 'dgn':'dengan',
    'emang':'memang', 'gw': 'saya', 'gak': 'tidak', 'hny':'hanya', 
    'hr':'hari', 'indo':'indonesia', 'jg': 'juga','jgn':'jangan', 
    'justeru':'justru', 'karna':'karena', 'klo':'jika', 'kpd':'kepada', 
    'lbh':'lebih', 'masy':'masyarakat', 'mak':'ibu', 'mjd':'menjadi', 
    'org':'orang', 'ora':'tidak', 'pake':'pakai', 'prodak':'produk', 
    'repoblik':'republik', 'sy':'saya', 'sma':'sama', 'spt':'seperti', 
    'tak':'tak', 'tau':'tahu', 'tdk':'tidak', 'tlsn':'tulis', 
    'ummat':'umat', 'utk':'untuk', 'jenderal':'jendral', 'prof':'profesor',
    'ttg':'tentang','dg':'dengan', 'dlm':'dalam', 'untk':'untuk', 
    'udah':'sudah', 'gue':'saya', 'jd':'jadi', 'kau':'kamu',
    'rame':'ramai', 'doang':'saja', 'ga':'tidak', 'bener':'benar', 
    'lu':'kamu', 'sdh':'sudah','gimana':'bagaimana', 'krn':'karena'
}

indo_stopwords = set(stopwords.words('indonesian'))
tambahan_stopwords = {'y', 'yg', 'nih', 'deh', 'banget', 'kayak', 'sih', 'amp', 
                      'aguanrasis', 'oocrp', 'tuh', 'kades', 'psn', 'tifa', 'mas', 'ppn', 
                      'sang', 'gitu', 'kader', 'kena', 'part', 'dki', 'gara', 'ruf', 
                      'gus', 'ya', 'bg', 'tlsn', 'sdm', 'sda', 'h', 'ri', 'adl', 'bin', 
                      'nya', 'kali', 'ribu', 'tuju', 'milu', 'swt', 'rp', 'kait', 'tim', 
                      'tol', 'm', 'pm', 'bs', 'untk', 'utk', 'bang', 'tp', 'sdh', 'dlm', 
                      'of', 'hut', 'pt', 'e', 'pd', 'a', 'ttg', 'si', 'ayo', 'dg', 'jkw', 
                      'sgb', 'udah', 'th', 'bin', 'era', 'kl', 'nya', 'jd', 'cs', 'jk', 
                      'bikin', 'uu', 'doang', 'om', 'tp', 't', 'ri', 'ma', 'an', 'sdh', 'no', 
                      'ps', 'sj', 'dll', 'dg', 'terna', 'pik', 'rusa', 'usak', 'tri', 
                      'uu', 'dar', 'lu', 'moga', 'cc'}
indo_stopwords = set(stopwords.words('indonesian'))
indo_stopwords.update(tambahan_stopwords)
indo_stopwords.discard('tidak')  # hapus 'tidak' jika ada  

tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-lite-base-p1")

def preprocess_text(text):
    # Hapus mention, hashtag, url
    text = re.sub(r"@\w+|#\w+|http\S+|www\S+", " ", text)
    # Hapus karakter non-alfabet, lowercase, dan spasi ganda
    text = re.sub(r"[^a-zA-Z\s]", " ", text).lower()
    text = re.sub(r"\s+", " ", text).strip()
    # Normalisasi slang
    text = normalize_text(text, slang_dictionary)
    # Tokenisasi awal untuk stopword removal
    tokens = text.split()
    tokens = [word for word in tokens if word not in indo_stopwords]
    cleaned_text = " ".join(tokens)
    # Tokenisasi menggunakan IndoBERT tokenizer
    tokens = tokenizer.tokenize(cleaned_text)
    return tokenizer.convert_tokens_to_string(tokens)

# Mapping label
label_mapping = {0: 'toleran', 1: 'intoleran'}

def predict_sentiment(text):
    processed = preprocess_text(text)
    tfidf_input = vectorizer.transform([processed])
    pred = model.predict(tfidf_input)[0]
    proba = model.predict_proba(tfidf_input)[0]
    return label_mapping[pred], proba

# Untuk batch: keluarkan 3 kolom
def predict_to_tuple(text):
    label, proba = predict_sentiment(text)
    return label, proba[0], proba[1]

def render():
    st.header("🧠 Intolerant Analysis")
    
    # Informasi penggunaan aplikasi
    st.markdown("""
    ### 📘 Panduan Penggunaan Aplikasi

    Aplikasi ini digunakan untuk **menganalisis dan mengklasifikasikan teks** sebagai *toleran* atau *intoleran* berdasarkan kontennya.  
    Terdapat dua jenis fitur klasifikasi yang bisa digunakan:

    #### 1. 🤖 Klasifikasi Satu Kalimat
    - Cocok untuk menguji satu kalimat atau teks pendek.
    - Masukkan kalimat di kolom teks yang disediakan.
    - Sistem akan menampilkan hasil klasifikasi beserta probabilitasnya.

    **Contoh input:**  
    `"Semua agama harus dihormati."`

    #### 2. 📂 Klasifikasi Batch via CSV
    - Cocok untuk mengklasifikasikan banyak teks sekaligus.
    - Unggah file **CSV** dengan kolom bernama `full_text` yang berisi kalimat-kalimat yang ingin diklasifikasikan.
    - Sistem akan membersihkan data, memproses, menampilkan hasil, dan menyediakan file hasil untuk diunduh.

    **Contoh isi file CSV:** Setelah membaca panduan di atas, silakan pilih mode klasifikasi di bawah ini.""")

    # Pilihan mode klasifikasi
    mode = st.radio("🛠️ Pilih mode klasifikasi:", ["Klasifikasi Satu Kalimat", "Klasifikasi Batch via CSV"])

    st.markdown("---")

    if mode == "Klasifikasi Satu Kalimat":
        st.subheader("🤖 Klasifikasi Satu Kalimat")
        classify_input = st.text_area("Masukkan kalimat untuk diklasifikasikan:", key="classify_input", height=120)
        if st.button("Klasifikasikan"):
            if not classify_input.strip():
                st.warning("Silakan masukkan teks terlebih dahulu.")
            else:
                label, probs = predict_sentiment(classify_input)
                st.markdown("**Hasil Klasifikasi:**")
                st.write(f"- Label: **{label.capitalize()}**")
                st.write(f"- Toleran: {probs[0]:.2%}")
                st.write(f"- Intoleran: {probs[1]:.2%}")

    elif mode == "Klasifikasi Batch via CSV":
        st.subheader("📂 Klasifikasi Batch via CSV")
        file = st.file_uploader("Unggah file CSV yang berisi kolom 'full_text':", type=["csv"])
        if file:
            df = pd.read_csv(file)

            if 'full_text' not in df.columns:
                st.error("Kolom 'full_text' tidak ditemukan di dalam file CSV.")
                st.stop()

            # Preprocessing
            df['cleaned_data'] = df['full_text'].astype(str).apply(preprocess_text)

            try:
                hasil = df['cleaned_data'].map(predict_to_tuple)
                df['Label'], df['Prob_Toleran'], df['Prob_Intoleran'] = zip(*hasil)

                # Susun kolom
                ordered_cols = ['cleaned_data', 'Label', 'Prob_Intoleran', 'Prob_Toleran', 'full_text']
                remaining_cols = [col for col in df.columns if col not in ordered_cols]
                df_final = df[ordered_cols + remaining_cols]

                # Tampilkan hasil
                st.markdown("**Hasil Klasifikasi (Batch):**")
                st.dataframe(df_final)

                # Unduh hasil
                csv_out = df_final.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Unduh Hasil CSV",
                    data=csv_out,
                    file_name='hasil_klasifikasi.csv',
                    mime='text/csv'
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses CSV: {e}")
