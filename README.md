# Hong Kong Instagram Username Classification

![alt text](ig-logo.png)

**Instagram** is a widely popular social media platform in Hong Kong as well as in the rest of the world. Therefore, if we are able to identify Hong Kong Instagram users from the large pool of users worldwide, company resources allocation and marketing strategies can significantly become more efficient and effective from a business perspective. A real-life implementation can be developing an Instagram advertising bot that exclusively targets and engages with users in Hong Kong.

In this individual machine learning project, I have taken an approach on exploring the feasibility of classifying the Hong Kong Instagram users solely based on the usernames. 

Scikit-learn's **Logistic Regression**, **Random Forest** and **SVM** are chosen as the baseline models and the training data of this project is scraped from [HypeAuditor](https://hypeauditor.com/) using my own web scraper **hypeauditor_scraper.py**.

## How does the Classification Work?

The core principle of this classification task revolves around the behavior of the NLTK syllable tokenizer and the distinctive linguistic features of Romanized Cantonese.        

Notably, the NLTK syllable tokenizer is not Cantonese-specific, but it could still provide a workaround by capturing some distintive patterns based on the behavior of the NLTK tokenizer, albeit the lack of Cantonese word embeddings.

The following is the visualization of the top 10 most appeared syllables in HK and Non-HK usernames:

![alt text](freq_chart.png)

> Terminologies:
>
> * **Vowels**: a,e,i,o,u,y* and can be a standalone syllable
> * **Consonants**: characters that are not vowels and cannot be a standalsone syllable
> * **Consonant-vowel (CV) syllables**: a syllable that contain both vowel and consonants, e.g. 'fi', 'ha', etc.
> * **Monosyllabic**: single/ one syllable
> 
> *Note: y sometimes can act as a vowel as well*

1. **Higher Appearance of standalone Vowels in HK** -> Unique Vowel Clusters
    * Romanized Cantonese has a lot of unique adjacent vowels compared to English or other languages
    * for example: {"張": "ch-***eu***-ng", "楊": "  ***yeu***-ng", "趙": "ch-***iu***", "游": "  ***yau***", ...}
    * the tokenizer is not familiar with these clusters and might treat them as an individual syllable

2.  **Less CV syllables, more Unique Syllables in HK**-> Complex Consonants Clusters
    * Romanized Cantonese also has a lot of complex consonants combinations and some can even contain no vowels at all.
    * for example : {"翠": "***ts***-ui", "芷": "  ***tsz***", "吳": "***ng***", "郭": "***kw***-ok", ...}
    * this confuses the tokenizer to group the consonants to other vowels, resulting in more unique syllables

3. **Lower Frequency of a syllable in HK** -> Monosyllabic Chinese Characters
    * the maximum frequency of a syllable is around 75 ("ha") in Non-HK while it is only roughly 50 ("i") in HK 
    * Hong Kong People's name are mostly made up of 3 Chinese characters, and each chinese character only has one syllable
    * i.e. Hong Kong People's name at most have 3 syllables and leads to overall lower frequency of syllables in usernames

All these differences contributed as the patterns for the models to identify HK usernames from non-HK usernames.

## Why Syllable Tokenizer?

Tokenization is a vital part in Natural Language Processing (NLP), as it involves breaking down a text into smaller units called tokens to act as the features for the model to do classification. Conventional tokens can be words, sentences, or even subword units. On the contrary, syllabic tokenization is regarded as a rather "inconsistent" tokenization technique since the phonetics in the English language is also "inconsistent", like knife and colonel. 

Nonetheless, I found that syllabic tokenization is still the most suitable choice in classifying usernames with the following reasons:

1. **No whitespaces between words** 
    * Lack of whitespaces in the Instagram usernames makes the traditional tokenizers that heavily rely on whitespaces cannot work properly.

2. **Usernames are not sentences**
    * In other words, usernames are too short to extract a "word" as a unit for the features.

3. **Usernames are not proper English**
    * Usernames are not proper English vocabularies, any conventional tokenizers will not have the word embeddings for usernames, so a subword tokenizer that tokenizes a word based on the prefixes and suffixes would also not work.

4. **No Cantonese-specific tokenizer**
    * The crucial reason to use syllable tokenizer is the absence of a pretrained Romanized Cantonese tokenizer. As demonstrated in the last part, syllabic tokenization can somehow identify some unique patterns based on the behavior of the NLTK tokenizer.        

> *learn more in [Forbidden Spellings](https://www.youtube.com/shorts/3ipFdRfFvK4) & [NLP pipeline deep dive: Why doesn't anyone tokenize by syllables?](https://www.youtube.com/watch?v=4_KxnoMnVVs&t=2990s&ab_channel=RachaelTatman)*

## Results

![alt text](confusion_matrix.png)

After tuning the hyperparameters and conducting validations, it was found that both **Logistic Regression (LR)** and **Support Vector Machines (SVM)** yielded the best testing results with **0.742**. On the other hand, Random Forest (RF) with 0.691  showed the worst performance due to potential underfitting or overfitting.

In the end, **SVM** was chosen over LR for actual deployment due to its **scalability**. Although they show a similar performance, as the dataset grows larger, LR may face challenges in capturing non-linear relationships of the syllables effectively. On the other hand, SVM is capable of handling non-linear relationships and can scale well to accommodate larger datasets with well-tuned hyperparameters and the kernel trick. However, if simplicity and computational cost are the main concerns, LR might be a more suitable choice to work with a small dataset. 

## Conclusion

In summary, this project demonstrates the classification of Hong Kong Instagram usernames, in which the **SVM** model is achieving a **74.2% accuracy**, using an unconventional tokenization technique based on syllables. The core principle of this classification task revolves around the behavior of the NLTK syllable tokenizer and the distinctive linguistic features of Romanized Cantonese.

Nevertheless, identifying usernames is a challenging topic and it is still important to acknowledge the limitations of this classification approach, such as the presence of public accounts, the inclusion of English names in HK users' usernames, and the variability in Romanized Chinese. Moreover, to enhance the model's performance, consider expanding the dataset, developing a Cantonese-specific tokenizer, and incorporating users' Instagram bios for improved classification results. 

> *please consider checking out **hk_ig_clf.ipynb** for full details. Thank You!!*



