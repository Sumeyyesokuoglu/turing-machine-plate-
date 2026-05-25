Turing Makinesi ile Araç Plaka Formatı Tanıyıcı

Bu depo, Otomata Teorisi ve Biçimsel Diller dersi kapsamında, deterministik bir Turing Makinesi (DTM) modeli kullanarak araç plaka formatlarını doğrulayan bir Python kodu içermektedir.

 1. Problem Tanımı
Otopark giriş sistemleri, Elektronik Denetleme Sistemleri (EDS) ve trafik kameraları gibi gerçek dünya uygulamalarında, gelen plaka verisinin belirli bir formata uygun olup olmadığını kontrol etmemiz gerekir.
Bu projede, bir girdinin yapısal olarak geçerliliği, en temel donanım soyutlama seviyesi olan Turing Makinesi modeli ile durum geçişleri kullanılarak modellenmiştir. Makine, banda yerleştirilen karakterleri soldan sağa doğru tarayarak kontrol eder ve girdiyi KABUL veya RED durumuna ulaştırır.

 3. Tanınan Dil ve Format Tanımı
Tasarlanan Turing Makinesi, Türkiye'deki standart plaka formatlarından birini temsil eden L dilini tanımak üzere kurgulanmıştır:
Format: NNLLNNN
Burada:
- N: Bir rakamı ifade eder (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
- L: Bir büyük harfi ifade eder (A'dan Z'ye kadar)

 Kritik Tasarım Gereksinimleri
Girdinin GEÇERLİ (KABUL) sayılabilmesi için aşağıdaki kısıtlamalar yüksek seviyeli dil fonksiyonları
(Örneğin: if len(plaka) == 7) kullanılmadan, tamamen Turing durumları ile doğrulanmalıdır:
1. Girdi uzunluğu tam olarak 7 karakter olmalıdır.
2. İlk iki karakter kesinlikle rakam (N) olmalıdır.
3. Üçüncü ve dördüncü karakter kesinlikle büyük harf (L) olmalıdır. Küçük harfler kesinlikle reddedilir.
4. Son üç karakter kesinlikle rakam (N) olmalıdır.
5. Eksik karakter, fazla karakter veya yanlış yerde yanlış karakter türünün bulunması durumunda makine anında RED durumuna geçmelidir.

 3. Turing Makinesi Matematiksel Modeli
Geliştirilen proje, biçimsel diller teorisindeki 7'li ile gösterilir:

M = (Q, Sigma, Gamma, Delta, q0, q_accept, q_reject)

- Q (Durumlar Kümesi): {q0, q1, q2, q3, q4, q5, q6, q7, q_red}
- Sigma (Giriş Alfabesi): {0-9, A-Z}
- Gamma (Bant Alfabesi): {0-9, A-Z, _} (Burada '_' sembolü Boşluk/Blank durumunu ifade eder)
- q0 (Başlangıç Durumu): q0
- q_accept (Kabul Durumu): q7
- q_reject (Red Durumu): q_red
 4. Durumların Açıklaması ve Çalışma Mantığı
Makine üzerindeki durumlar plaka üzerindeki karakter konumlarıyla ardışık olarak eşleşir:

- q0: İlk karakteri okur. Eğer rakam (N) ise Sağ (R) yönüne gider ve q1 durumuna geçer. Aksi halde q_red durumuna geçer.
- q1: İkinci karakteri okur. Eğer rakam (N) ise Sağ (R) yönüne gider ve q2 durumuna geçer. Aksi halde q_red durumuna geçer.
- q2: Üçüncü karakteri okur. Eğer büyük harf (L) ise Sağ (R) yönüne gider ve q3 durumuna geçer. Aksi halde q_red durumuna geçer.
- q3: Dördüncü karakteri okur. Eğer büyük harf (L) ise Sağ (R) yönüne gider ve q4 durumuna geçer. Aksi halde q_red durumuna geçer.
- q4: Beşinci karakteri okur. Eğer rakam (N) ise Sağ (R) yönüne gider ve q5 durumuna geçer. Aksi halde q_red durumuna geçer.
- q5: Altıncı karakteri okur. Eğer rakam (N) ise Sağ (R) yönüne gider ve q6 durumuna geçer. Aksi halde q_red durumuna geçer.
- q6: Yedinci karakteri okur. Eğer rakam (N) ise Sağ (R) yönüne gider ve q7 durumuna geçer. Aksi halde q_red durumuna geçer.
- q7: Sekizinci karakteri kontrol eder. Eğer boşluk ('_') okursa, girdi tam olarak 7 karakter demektir ve makine DURUR ve KABUL EDER. Eğer boşluk dışında başka bir karakter varsa (fazla karakter durumu) q_red durumuna geçilir.
- q_red: Herhangi bir format ihlalinde bu duruma gelinir ve makine DURUR ve REDDEDER.



