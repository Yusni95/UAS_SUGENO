#Nama   : Muhammad Yusni Ardian
#NIM    : 191011401665
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : Permintaan Pencucian Drum Minyak

#Kecepatan Debit Air : min 4 liter/detik dan max 6 liter/detik.
#Banyaknya Drum  : sedikit 50 dan banyak 200.
#Tingkat Kekotoran Drum : rendah 40, sedang 50, dan 60 tinggi.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Drum():
    minimum = 50
    maximum = 200

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class Kotor():
    minimum = 40
    medium = 50
    maximum = 60

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class Debit():
    minimum = 4
    maximum = 6
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_Drum, jumlah_kotor):
        drm = Drum()
        ktr = Kotor()
        result = []
        
        # [R1] Jika Drum SEDIKIT, dan Kotor RENDAH, 
        #     MAKA Debit = 4
        α1 = min(drm.sedikit(jumlah_Drum), ktr.rendah(jumlah_kotor))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Drum SEDIKIT, dan Kotor SEDANG, 
        #     MAKA Debit = 10 * jumlah_kotor + 100
        α2 = min(drm.sedikit(jumlah_Drum), ktr.sedang(jumlah_kotor))
        z2 = 10 * jumlah_kotor + 100
        result.append((α2, z2))

        # [R3] Jika Drum SEDIKIT, dan Kotor TINGGI, 
        #     MAKA Debit = 10 * jumlah_kotor + 200
        α3 = min(drm.sedikit(jumlah_Drum), ktr.tinggi(jumlah_kotor))
        z3 = 10 * jumlah_kotor + 200
        result.append((α3, z3))

        # [R4] Jika Drum BANYAK, dan Kotor RENDAH,
        #     MAKA Debit = 6 * jumlah_Drum + 2 * jumlah_kotor
        α4 = min(drm.banyak(jumlah_Drum,), ktr.rendah(jumlah_kotor))
        z4 = 5 * jumlah_Drum + 2 * jumlah_kotor
        result.append((α4, z4))

        # [R5] Jika Drum BANYAK, dan Kotor SEDANG,
        #     MAKA Debit = 5 * jumlah_Drum + 4 * jumlah_kotor + 100
        α5 = min(drm.banyak(jumlah_Drum), ktr.sedang(jumlah_kotor))
        z5 = 5 * jumlah_Drum + 4 * jumlah_kotor + 100
        result.append((α5, z5))

        # [R6] Jika Drum BANYAK, dan Kotor TINGGI,
        #     MAKA Debit = 5 * jumlah_Drum + 5 * jumlah_kotor + 300
        α6 = min(drm.banyak(jumlah_Drum), ktr.tinggi(jumlah_kotor))
        z6 = 5 * jumlah_Drum + 5 * jumlah_kotor + 300
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_Drum, jumlah_kotor):
        inferensi_values = self.inferensi(jumlah_Drum, jumlah_kotor)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])