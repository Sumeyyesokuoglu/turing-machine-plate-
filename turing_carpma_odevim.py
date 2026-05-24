class TuringMachine:
    def __init__(self, carpan1: str, carpan2: str):
        bellek_alani = (len(carpan1) + 2) * (len(carpan2) + 2) + 50
        self.tape = list(f"{carpan1}*{carpan2}=") + ['_'] * bellek_alani
        self.head = 0
        self.state = 'q_tara_carpilan'  # q0 -> q_tara_carpilan
        self.step_count = 0

        self.gecici_toplam = ''
        self.yazilan_indeks = 0
        self.son_bit_mi = False 

    def _bant_metni(self) -> str:
        return "".join(self.tape)

    def print_step(self, okunan_sem, yazilan_sem, yon, anlik_durum):
        # Okunan ve yazılan semboller boşluk ise tabloda B olarak gösterilsin
        gosterim_okunan = 'B' if okunan_sem == '_' else okunan_sem
        gosterim_yazilan = 'B' if yazilan_sem == '_' else yazilan_sem

        saf_bant = self._bant_metni().rstrip('_')
        
        if self.head >= len(saf_bant):
            saf_bant = saf_bant.ljust(self.head + 1, '_')
        
        # Sadece ekrana basılırken alt çizgiler B harfine dönüştürülüyor
        saf_bant = saf_bant.replace('_', 'B')
        
        gosterim = (
            saf_bant[:self.head]
            + "[" + saf_bant[self.head] + "]"
            + saf_bant[self.head + 1:]
        )
        print(f" {anlik_durum:<18} | {gosterim_okunan:^7} | {gosterim_yazilan:^10} | {yon:^7} | {gosterim}")

    def read(self):
        while self.head >= len(self.tape):
            self.tape.append('_')
        return self.tape[self.head]

    def write(self, sembol):
        while self.head >= len(self.tape):
            self.tape.append('_')
        self.tape[self.head] = sembol

    def move(self, yon):
        if yon == 'R':
            self.head += 1
        elif yon == 'L':
            self.head = max(0, self.head - 1)

    def _oku_carpilan(self):
        metin = self._bant_metni()
        sol_kisim = metin.split('*')[0]
        return ''.join(s for s in sol_kisim if s in '01') or '0'

    def _oku_mevcut_sonuc(self):
        metin = self._bant_metni()
        parcalar = metin.split('=')
        sag_kisim = parcalar[1] if len(parcalar) > 1 else ''
        return ''.join(s for s in sag_kisim if s in '01') or '0'

    def _sola_kaydir_carpilan(self):
        metin = self._bant_metni()
        yildiz_yeri = metin.index('*')
        mevcut = ''.join(s for s in metin[:yildiz_yeri] if s in '01')
        yeni_hali = (mevcut + '0').lstrip('0') or '0'
        
        hizalanmis = yeni_hali.zfill(yildiz_yeri)
        if len(hizalanmis) > yildiz_yeri:
            fark = len(hizalanmis) - yildiz_yeri
            self.tape = list(' ' * fark) + self.tape
            self.head += fark
            metin2 = "".join(self.tape)
            yildiz_yeri = metin2.index('*')
            
        for idx, kar in enumerate(hizalanmis):
            self.tape[idx] = kar

    def run(self):
        print("Turing Simülasyonu Akışı Başlatılıyor...\n")
        
        # Tablo Başlığı (Durum alanı genişletildi)
        print("-" * 105)
        print(f" {'DURUM':<18} | {'OKUNAN':^7} | {'YAZILAN':^10} | {'YÖN':^7} | {'BANT İÇERİĞİ'}")
        print("-" * 105)

        LIMIT = 25000

        while self.step_count < LIMIT:
            okunan = self.read()
            yazilacak = okunan
            hareket_yonu = 'S'
            eski_durum = self.state

            if self.state in ('q_kabul', 'q_red'):
                self.print_step(okunan, yazilacak, 'S', eski_durum)
                break

            # q_tara_carpilan (Eski q0): Birinci sayının üzerinden sağa tarama
            elif self.state == 'q_tara_carpilan':
                if okunan in ('0', '1'):
                    hareket_yonu = 'R'
                elif okunan == '*':
                    self.state = 'q_tara_carpan'
                    hareket_yonu = 'R'
                else:
                    self.state = 'q_red'

            # q_tara_carpan (Eski q1): İkinci sayının üzerinden '=' karakterine kadar sağa tarama
            elif self.state == 'q_tara_carpan':
                if okunan in ('0', '1'):
                    hareket_yonu = 'R'
                elif okunan == '=':
                    self.state = 'q_bit_ara'
                    hareket_yonu = 'L'
                else:
                    self.state = 'q_red'

            # q_bit_ara (Eski q2): Çarpanın işlenmemiş sağdaki ilk bitini arama ve maskeleme (X/Y)
            elif self.state == 'q_bit_ara':
                if okunan in ('X', 'Y'):
                    hareket_yonu = 'L'

                elif okunan == '0':
                    yazilacak = 'Y'
                    is_last = (self.tape[self.head - 1] == '*')
                    self.son_bit_mi = is_last
                    if is_last:
                        self.state = 'q_temizle_git'
                    else:
                        self.state = 'q_kaydir_git'
                    hareket_yonu = 'L'

                elif okunan == '1':
                    yazilacak = 'X'
                    is_last = (self.tape[self.head - 1] == '*')
                    self.son_bit_mi = is_last

                    c1 = self._oku_carpilan()
                    c2 = self._oku_mevcut_sonuc()
                    hesap = int(c1, 2) + int(c2, 2)
                    self.gecici_toplam = bin(hesap)[2:]
                    self.yazilan_indeks = 0

                    self.state = 'q_esittir_ara_ekle'
                    hareket_yonu = 'R'

                elif okunan == '*':
                    self.state = 'q_temizle_git'
                    hareket_yonu = 'L'
                else:
                    self.state = 'q_red'

            # q_esittir_ara_ekle (Eski q3): Ekleme yapmak için sağa doğru '=' işaretini arama
            elif self.state == 'q_esittir_ara_ekle':
                if okunan != '=':
                    hareket_yonu = 'R'
                else:
                    self.state = 'q_toplam_yaz'
                    hareket_yonu = 'R'

            # q_toplam_yaz (Eski q4): Geçici toplamı '=' işaretinin sağına yazdırma
            elif self.state == 'q_toplam_yaz':
                if self.yazilan_indeks < len(self.gecici_toplam):
                    yazilacak = self.gecici_toplam[self.yazilan_indeks]
                    self.yazilan_indeks += 1
                    hareket_yonu = 'R'
                else:
                    self.state = 'q_esittir_don'
                    hareket_yonu = 'L'

            # q_esittir_don (Eski q5): Yazım bitince sola, tekrar '=' işaretine dönme
            elif self.state == 'q_esittir_don':
                if okunan != '=':
                    hareket_yonu = 'L'
                else:
                    if self.son_bit_mi:
                        self.state = 'q_temizle_git'
                    else:
                        self.state = 'q_kaydir_git'
                    hareket_yonu = 'L'

            # q_kaydir_git (Eski q6): Sola kaydırmayı tetiklemek için '=' işaretine sağdan yaklaşma
            elif self.state == 'q_kaydir_git':
                if okunan != '=':
                    hareket_yonu = 'R'
                else:
                    self._sola_kaydir_carpilan()
                    if self.son_bit_mi:
                        self.state = 'q_temizle_git'
                    else:
                        self.state = 'q_bit_ara'
                    hareket_yonu = 'L'

            # q_temizle_git (Eski q7): Temizlik aşaması için '*' işaretine kadar sola gitme
            elif self.state == 'q_temizle_git':
                if okunan != '*':
                    hareket_yonu = 'L'
                else:
                    self.state = 'q_maske_temizle'
                    hareket_yonu = 'R'

            # q_maske_temizle (Eski q8): Maskeleri (X/Y) kaldırıp bandı orijinal haline getirme ve kabul etme
            elif self.state == 'q_maske_temizle':
                if okunan == 'X':
                    yazilacak = '1'
                    hareket_yonu = 'R'
                elif okunan == 'Y':
                    yazilacak = '0'
                    hareket_yonu = 'R'
                elif okunan == '=':
                    self.state = 'q_kabul'
                    hareket_yonu = 'S'
                else:
                    hareket_yonu = 'R'
            else:
                self.state = 'q_red'

            self.write(yazilacak)
            self.print_step(okunan, yazilacak, hareket_yonu, eski_durum)
            self.move(hareket_yonu)
            self.step_count += 1
        else:
            print(f"\nUYARI: {LIMIT} adım sınırı aşıldığı için simülasyon kesildi!")

# ----------------------------------------------------------------------
def main():
    print("-" * 65)
    print("      TURING CALCULATOR - BINARY MULTIPLICATION MODEL")
    print("-" * 65)

    girdi1 = input("1. Binary Değeri Giriniz: ").strip()
    girdi2 = input("2. Binary Değeri Giriniz: ").strip()

    if not girdi1 or not girdi2:
        print("Hata: Girdilerden biri veya ikisi boş bırakılamaz!")
        return
    if not all(k in '01' for k in girdi1) or not all(k in '01' for k in girdi2):
        print("Hata: Sadece ikili sistem sayıları (0-1) kabul edilir!")
        return

    dogrulama_sonucu = int(girdi1, 2) * int(girdi2, 2)
    print(f"\nOluşturulan Bant Formatı: {girdi1}*{girdi2}=")
    print(f"Beklenen Matematiksel Çıktı: {dogrulama_sonucu} ({bin(dogrulama_sonucu)[2:]})\n")

    makine = TuringMachine(girdi1, girdi2)
    makine.run()

    print("-" * 105)  # Tabloyu kapatma çizgisi

    # En alttaki özet bilgisinde de boşluklar B olarak değiştirildi
    bant_son_hali = "".join(makine.tape).rstrip('_').replace('_', 'B')
    kesim = bant_son_hali.split('=')
    nihai_raw = kesim[1] if len(kesim) > 1 else ''
    nihai_binary = ''.join(s for s in nihai_raw if s in '01') or '0'
    nihai_decimal = int(nihai_binary, 2)

    print("\n" + "~" * 65)
    print("SİMÜLASYON BAŞARIYLA TAMAMLANDI")
    print("~" * 65)
    print(f"Bandın Son İçeriği  : {bant_son_hali}")
    print(f"Harcanan Adım Sayısı: {makine.step_count}")
    print(f"Sonuç (İkilik)      : {nihai_binary}")
    print(f"Sonuç (Onluk)       : {nihai_decimal}")
    print(f"Kontrol Mekanizması : {int(girdi1,2)} x {int(girdi2,2)} = {dogrulama_sonucu}")

if __name__ == "__main__":
    main()