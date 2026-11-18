# SDK Final — Instructor live-coding guide (120 min)

**الهدف:** الطلاب يشوفوا الكود اللي تعلموه من Pandas لـ NLP، وكيف Streamlit بتعرض **البيانات والخطوات والنتائج والـLogs**، ثم ينشروا رابط شغال.

### 0–10 دقيقة | الفكرة والـDataset
- افتحي Kaggle: https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews
- نزلي CSV، وخلي الطلاب يعرفوا ليش الداتا مناسبة: Numeric (Age), Categorical (Department Name), Text (Review Text), Rating for EDA.
- احكي: "مش هدفنا نعمل Model. بدنا نعمل تطبيق يفرجي شو صار للداتا، وكيف نعرف إذا كل خطوة نجحت."

### 10–25 دقيقة | من Colab إلى ملفات Python
- اشرحي `engine.py` مقابل `app.py`: واحد للمنطق والثاني للواجهة.
- شغّلي تجربة `quality_report(df)` من Colab أو Python وورجيهم نفس الناتج داخل Streamlit.
- اسألي: ليش ما بنحط كل كود الـCleaning داخل `app.py`؟

### 25–45 دقيقة | Streamlit + EDA
- اشرحي `st.title`, `st.file_uploader`, `st.metric`, `st.dataframe`, `st.plotly_chart`.
- الطلاب يرفعوا Kaggle CSV ويتابعوا Missing Chart وRating Chart وDepartments.
- Task: شو الفرق بين `Clothing ID` و`Age`؟ وليش ما بنعمل Scale للأول؟

### 45–70 دقيقة | Cleaning + Pipelines
- افتحي `engine.py`: `clean_text()` و`build_pipeline()` و`run_pipeline()`.
- تاب Pipeline Builder: اختاري Age وPositive Feedback Count، ثم Department Name وClass Name، ثم Review Text.
- اسأليهم يتوقعوا شكل الـOutput، ثم شغلي. فسّري `SimpleImputer`, `StandardScaler`, `OneHotEncoder`, `TfidfVectorizer`.
- Task: غيروا Text Column أو ألغوها، وشوفوا عدد Features يتغير كيف.

### 70–90 دقيقة | Logging + Results
- ورجي `logging.basicConfig()` ومستويات `INFO`, `WARNING`, `ERROR`.
- اضغطي Run، روحي Results & Logging، واقرأي الـSteps من 1/6 إلى 6/6.
- قارني Missing قبل وبعد، والـRaw/Cleaned Review، وMatrix Preview.
- Task: اختاري Review Column كلها فارغة بعينة تدريبية وشوفي رسالة الخطأ المناسبة.

### 90–110 دقيقة | GitHub + Publish
- ارفعي ملفات `app.py`, `engine.py`, `requirements.txt`, `data/` إلى Repo.
- افتحي https://share.streamlit.io → Create app → Existing app → GitHub repo → `app.py` → Deploy.
- انتظري تطبيق واحد على الأقل يشتغل أمام الطلاب، وارفعي CSV في النسخة المنشورة.

### 110–120 دقيقة | Independence challenge
- خلي الطلاب يغيّروا اختيار الأعمدة ويعيدوا التشغيل، ويفسروا WARNING واحدة وINFO واحدة.
- المطلوب بالفاينال: رابط Streamlit + رابط GitHub + لقطة Results & Logs + جملة تشرح Pipeline.

## أسئلة مناقشة سريعة
1. شو الفرق بين `fit_transform()` و `transform()`؟
2. ليش ما شلنا `not` من المراجعات؟
3. لو المستخدم اختار Text Column، شو بتضيف TF-IDF؟
4. ليش Logging مفيدة حتى لو الرسومات اشتغلت؟
5. هل مشروعنا يتنبأ بـRecommended IND؟ **لا**، هذا Data Preparation فقط.

## خطة بديلة لو الوقت ضاق
جهزي GitHub Repo قبل الدرس، وخلي الطلاب يبنوا `clean_text` و`quality_report` معك، وباقي الـFiles من Starter Code. خصصي آخر 20 دقيقة للنشر بدل ما تضيعيها بالتثبيت. وخلي عينة SDK جاهزة لو تحميل Kaggle تأخر.
