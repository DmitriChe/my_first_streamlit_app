import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# фильтрация предупреждений:
import warnings
warnings.filterwarnings('ignore')

# Название приложения
st.title('Заполни пропуски!')

# Описание приложения
st.write('Загрузи свой датафрейм и заполни пропуски')


## Шаг 1. Загрузка CSV файла
# st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")
label = 'Загрузи CSV файл:'
uploaded_file = st.sidebar.file_uploader(label, type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head(5))
else:
    st.stop()

## Шаг 2. Проверка наличия пропусков в файле
missed_values = df.isna().sum()
missed_values = missed_values[missed_values > 0]
# st.write(missed_values)
# Проверка, что есть пропущенные значения:
if len(missed_values) > 0:
    fig, ax = plt.subplots()
    sns.barplot(x=missed_values.index, y=missed_values.values)
    ax.set_title('Пропуски в столбцах')
    # Передаем график на отрисовку в streamlit
    st.pyplot(fig)
## Шаг 3. Заполнить пропуски в файле

    button = st.button('Заполни пропуски')
    if button:
        df_filled = df[missed_values.index].copy()
        for col in df_filled.columns:
            if df_filled[col].dtype == 'object':  # категориальные признаки заполняем самым частым из них - модой
                df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
            else:  # если признак количественный, то заполняем медианой признака
                df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        st.write('Заполненный датафрейм:')
        st.write(df_filled.head(5))

## Шаг 4. Выгрузка заполненного от пропусков CSV файла
        download_button = st.download_button(label='Скачать файл CSV без пропусков',
                                             data=df_filled.to_csv(),
                                             file_name='filled_file.csv')
else:
    st.write('Нет пропусков в данных!')
    st.stop()





