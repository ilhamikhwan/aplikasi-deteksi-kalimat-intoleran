import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
from collections import Counter
import re
from nltk.corpus import stopwords
import nltk

def render():
    st.header("Analisis Data")

    nltk.download('stopwords')

    # Load dataset
    df = pd.read_csv("dataset_toleran_intoleran.csv", sep=';', encoding='latin-1')

    st.subheader("1. Jumlah Data")
    st.write(f"Jumlah Data Keseluruhan: {len(df)}")

    # 2. Pie Chart Distribusi Label
    st.subheader("2. Distribusi Label Toleran vs Intoleran")
    value_counts = df['label'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90, 
            colors=['#ff9999', '#66b3ff'], explode=(0.05, 0), shadow=True)
    ax1.axis('equal')
    st.pyplot(fig1)

    # 3. Distribusi Data Per Akun
    st.subheader("3. Distribusi Data per Kategori Akun")
    political_accounts = ['aniesbaswedan', 'jokowi', 'prabowo', 'mohmahfudmd', 'susipudjiastuti']
    buzzer_accounts = ['ArdieSuhardi321', 'CakNur971', 'OjolNyambi', 'H4T14K4LN4L42', 'PngAdilnR4kyt']
    username_mapping = {
        'aniesbaswedan': 'A',
        'jokowi': 'B',
        'prabowo': 'C',
        'mohmahfudmd': 'D',
        'susipudjiastuti': 'E',
        'ArdieSuhardi321': 'F',
        'CakNur971': 'G',
        'OjolNyambi': 'H',
        'H4T14K4LN4L42': 'I',
        'PngAdilnR4kyt': 'J'
    }
    df['user_category'] = df['username'].map(username_mapping)
    df['type'] = df['username'].apply(lambda x: 'Tokoh Politik' if x in political_accounts else 'Buzzer')
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    sns.countplot(data=df, x='user_category', hue='type', 
                  order=['A','B','C','D','E','F','G','H','I','J'], 
                  palette={'Tokoh Politik':'#1f77b4', 'Buzzer':'#ff7f0e'},
                  edgecolor='black', linewidth=1.2, alpha=0.9, ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # 4. Stacked Bar Plot Label per Akun
    st.subheader("4. Distribusi Konten Toleran vs Intoleran per Akun")
    fig3, ax3 = plt.subplots(figsize=(14, 7))
    df_grouped = df.groupby(['user_category', 'label']).size().unstack()
    df_grouped[['intoleran', 'toleran']].plot(kind='bar', stacked=True, 
                                              color=['#d62728', '#2ca02c'],
                                              edgecolor='#333333', linewidth=1,
                                              alpha=0.85, ax=ax3)
    plt.xticks(rotation=0)
    plt.title('Distribusi Konten Toleran vs Intoleran per Akun')
    st.pyplot(fig3)

    # 5 & 6. WordCloud Intoleran dan Toleran
    def process_text(text):
        text = re.sub(r'http\S+|@\w+|#\w+|[^\w\s]', '', text.lower())
        words = text.split()
        return [word for word in words if word not in stopwords.words('indonesian') and len(word) > 2]

    st.subheader("5. Word Cloud Intoleran")
    intoleran_words = df[df['label'] == 'intoleran']['full_text'].apply(process_text).explode()
    word_freq_intoleran = Counter(intoleran_words)
    wc1 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq_intoleran)
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.imshow(wc1, interpolation='bilinear')
    ax4.axis('off')
    st.pyplot(fig4)
    
    # Proses kata-kata dari label intoleran
    intoleran_words = df[df['label'] == 'intoleran']['full_text'].apply(process_text).explode()
    intoleran_freq = Counter(intoleran_words).most_common(10)
    intoleran_df = pd.DataFrame(intoleran_freq, columns=['Kata', 'Jumlah'])

    # Plot dalam Streamlit
    st.subheader("10 Kata Paling Umum dalam Konten Intoleran")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=intoleran_df, x='Kata', y='Jumlah', palette='Reds', ax=ax)
    ax.set_title('10 Kata Paling Umum dalam Konten Intoleran')
    ax.set_xlabel('Kata Kunci')
    ax.set_ylabel('Frekuensi Kemunculan')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("6. Word Cloud Toleran")
    toleran_words = df[df['label'] == 'toleran']['full_text'].apply(process_text).explode()
    word_freq_toleran = Counter(toleran_words)
    wc2 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq_toleran)
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    ax5.imshow(wc2, interpolation='bilinear')
    ax5.axis('off')
    st.pyplot(fig5)
    
    # Proses kata-kata dari label toleran
    toleran_words = df[df['label'] == 'toleran']['full_text'].apply(process_text).explode()
    toleran_freq = Counter(toleran_words).most_common(10)
    toleran_df = pd.DataFrame(toleran_freq, columns=['Kata', 'Jumlah'])

    # Plot dalam Streamlit
    st.subheader("10 Kata Paling Umum dalam Konten Toleran")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=toleran_df, x='Kata', y='Jumlah', palette='Greens', ax=ax)
    ax.set_title('10 Kata Paling Umum dalam Konten Toleran')
    ax.set_xlabel('Kata Kunci')
    ax.set_ylabel('Frekuensi Kemunculan')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    
    # Data performa
    data = {
        '50:50': {
            'metrics': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Linear': [95.9, 96.5, 95.2, 95.8],
            'Polynomial': [90.0, 98.0, 81.7, 89.0],
            'RBF': [94.9, 95.0, 94.6, 94.9],
            'Sigmoid': [95.2, 95.7, 94.6, 95.2]
        },
        '60:40': {
            'metrics': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Linear': [95.8, 96.9, 94.7, 95.8],
            'Polynomial': [89.5, 98.7, 80.1, 88.5],
            'RBF': [96.3, 96.9, 95.7, 96.3],
            'Sigmoid': [96.7, 97.6, 95.7, 96.7]
        },
        '70:30': {
            'metrics': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Linear': [95.8, 95.2, 96.5, 95.8],
            'Polynomial': [89.2, 97.8, 80.1, 88.1],
            'RBF': [95.4, 95.9, 94.6, 95.3],
            'Sigmoid': [96.0, 95.0, 96.9, 96.1]
        },
        '80:20': {
            'metrics': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Linear': [97.7, 97.4, 98.0, 97.7],
            'Polynomial': [89.7, 100, 79.5, 88.6],
            'RBF': [96.7, 97.0, 96.0, 96.7],
            'Sigmoid': [97.0, 96.0, 98.0, 97.0]
        },
        '90:10': {
            'metrics': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Linear': [98.7, 98.7, 98.7, 98.7],
            'Polynomial': [90.1, 100, 80.0, 88.9],
            'RBF': [98.7, 98.7, 98.7, 98.7],
            'Sigmoid': [98.7, 98.7, 98.7, 98.7]
        }
    }

    # Warna dan layout
    colors = ['#4E79A7', '#F28E2B', '#59A14F', '#E15759', '#BF00FF']
    bar_width = 0.18
    spacing = 0.08

    # Judul
    st.title("Analisis Performa Kernel SVM Berbagai Pembagian Data")

    # Visualisasi
    fig, axs = plt.subplots(3, 2, figsize=(25, 20))  # 3 baris x 2 kolom (1 slot kosong)
    axs = axs.flatten()

    for idx, (split_ratio, split_data) in enumerate(data.items()):
        ax = axs[idx]
        metrics = split_data['metrics']
        x = np.arange(len(metrics))

        for i, kernel in enumerate(['Linear', 'Polynomial', 'RBF', 'Sigmoid']):
            values = split_data[kernel]
            positions = x + i * (bar_width + spacing)
            bars = ax.bar(positions, values, bar_width,
                        color=colors[i],
                        edgecolor='black',
                        label=kernel)

            for pos, val in zip(positions, values):
                ax.text(pos, val + 0.5,
                        f'{val}%',
                        ha='center',
                        va='bottom',
                        fontsize=11,
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

        ax.set_title(f'Pembagian Data {split_ratio} Train:Test', fontsize=14, pad=10)
        ax.set_xticks(x + 1.5 * (bar_width + spacing))
        ax.set_xticklabels(metrics, fontsize=12)
        ax.set_ylim(75, 105)
        ax.set_yticks(np.arange(75, 101, 5))
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.axhline(90, color='gray', linestyle=':', linewidth=1, alpha=0.7)
        ax.axhline(95, color='blue', linestyle='--', linewidth=1, alpha=0.5)

    # Kosongkan subplot terakhir jika ada lebih dari 5
    if len(data) < len(axs):
        for i in range(len(data), len(axs)):
            axs[i].axis('off')

    # Legenda global
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(4)]
    fig.legend(handles, ['Linear', 'Polynomial', 'RBF', 'Sigmoid'],
            loc='lower center',
            ncol=4,
            bbox_to_anchor=(0.5, -0.01),
            fontsize=15,
            frameon=False)

    plt.tight_layout()
    st.pyplot(fig)
    
    
    # Warna kernel
    colors = ['#4E79A7', '#F28E2B', '#59A14F', '#E15759', '#BF00FF']

    # Judul halaman
    st.title("Tren Performa Kernel SVM per Metrik")

    # Buat plot
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    axs = axs.flatten()

    metric_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    ratios = ['50:50', '60:40', '70:30', '80:20', '90:10']
    kernel_names = ['Linear', 'Polynomial', 'RBF', 'Sigmoid']

    for i, metric in enumerate(metric_names):
        ax = axs[i]
        for j, kernel in enumerate(kernel_names):
            values = [data[ratio][kernel][i] for ratio in ratios]
            ax.plot(ratios, values, marker='o', color=colors[j], label=kernel)
        ax.set_title(metric)
        ax.set_ylim(75, 105)
        ax.grid(True)

    # Tambahkan legenda dan judul utama
    fig.suptitle('Tren Performa Kernel SVM per Metrik', fontsize=16)
    fig.legend(kernel_names, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.05), frameon=False)
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Tampilkan plot di Streamlit
    st.pyplot(fig)