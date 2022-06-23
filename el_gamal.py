import numpy as np
import random
from math import sqrt

XA=1
# mặc định khóa bí mật
q=2
# mặc định số nguyên tố
a=2
# mặc định phần tử sinh

# get và set các giá trị mặc định
def setXA(num):
    XA = num

def getXA():
    return XA

def setq(num):
    q=num

def getq():
    return q

def seta(num):
    a =num

def geta():
    return a
###########################################

# hàm nhân bình phương có lặp
def nhanBphuonLlap(x, y, p):
    res = 1  # giá trị khởi tạo

    x = x % p  # chia lấy dư x = x mod p

    while (y > 0):

        # nếu y là số lẻ thì res = (res * x) mod p
        if (y & 1):
            res = (res * x) % p

        # Nếu y chẵn thì y dịch phải 1 đơn vị (y = y/2)
        y = y >> 1  
        x = (x * x) % p

    return res

# hàm phân tích thừa só nguyên tố
def phanTichTSNT(s, n):
    # tìm số lần n chia hết cho 2
    while (n % 2 == 0):
        s.add(2)
        n = n // 2

    # chạy vòng for chỉ tìm các số lẻ 
    # (vì các số nguyên tố chỉ là các số lẻ)
    for i in range(3, int(sqrt(n)), 2):

        # nếu n chia hết cho i, tìm số lần n chia hết cho i
        while (n % i == 0):
            s.add(i)
            n = n // i

    # trường hợp đậc biệt n là số nguyên tố lớn hơn 2
    if (n > 2):
        s.add(n)


# hàm tìm phần tứ sinh (mặc định là 15)
def TimPhanTuSinh(n):
    s = set()

    # vì n là số nguyên tố nên phi = n - 1
    phi = n - 1

    # s là tập hợp thừa số nguyên tố của phi
    phanTichTSNT(s, phi)

    # ktra từ 2 đến phi
    for r in range(2, phi + 1):

        flag = False
        for it in s:

            # Ktra xem r^((phi)/primefactors) mod n = 1 hay ko
            if (nhanBphuonLlap(r, phi // it, n) == 1):
                flag = True
                break

        # nếu nhanBphuonLlap không ra =1.
        if (flag == False):
            return r


    # Nếu ko tìm thấy phần tử sinh
    return -1

#import randint as rand
#q = prime number  ////////// done

#a<q    a primitive root with q  /////////////done
#XA<q-1//done generated randomly
#YA=a^XA mod q //done
#public key pu = {q,a,YA}
#privatekey=XA

#q=10
#generaate prime number

def generate_public_key():

    while (1):
        q = random.randrange(100, 999)
        i = q - 1
        ct = 0

        while (i >= 5):
            if (q % i == 0):
                ct += 1
                break
            i -= 1

        if (ct == 0):
            print("sinh so ngto ngau nhien: q=", q)
            break

    # a primitive root with q

    # Driver Code

    a = 15#TimPhanTuSinh(q)
    seta(a)
    print("Phan tu sinh a= ", a)
    XA = random.randrange(0, q - 1)
    print("Khoa rieng duoc tao ra la XA(alpha)=", XA)
    # YA=a^XA mod q
    temp = a ** XA
    YA = temp % q


    publickey = [q, a, YA, XA]
    print("Khoa cong khai duoc tao ra la YA(beta) =",YA)
    print("============================================")
    #print("the public key is",publickey)
    return publickey

#generate_public_key()
#plain text    m<q
#select random integer k     k<q
#calculate K = YA^k mod q
#Calculate C1 = a^k mod q
#calculate C2 = KM mod q
#cipher text =(C1.C2)
def incrypt_gamal(q,a,YA,text):#{q, a, YA, XA}
    print("==================>start el_gammal encrypting")

    text=list(text)

    print(text)

    asc = []
    for i in range(len(text)):
        asc.append(ord(text[i]))
    # M=len(text)#M calc
    M = asc
    # random integer k
    k = random.randrange(0, q)
    print("tao so ngau nhien k:  ", k)
    # calculate K
    temp = YA ** k
    K = temp % q  # Kcalculated
    # tinh binh phuong co lap truoc cho viec di tim y2 trong thuat toan elgamal giai doan ma hóa
    # print("YA^k = ", K)

    temp = a ** k
    C1 = temp % q  # C1 calculated
    print("y1= ", C1)

    # C2 calculation

    C2 = []
    for i in range(len(M)):
        temp = K * M[i]
        out = temp % q
        C2.append(out)

    # temp = K*M
    # C2 = temp %q
    print("y2 = ", C2)
    chuoiMaHoa = ""
    chuoiMaHoa+= str(C1) + ","
    # chuoiMaHoa[0] = C1
    for i in range(len (C2)):
        chuoiMaHoa += str(C2[i])+","

    chuoiMaHoa+=  str(q)
    # chuoiMaHoa[-1] = p (vi tri cuoi cung trong chuoi)
    print("Ban ma y = (y1,y2) =  (",chuoiMaHoa,")")
    return chuoiMaHoa

#{m,k,K,C1,C2} done
#cipher text = (C1,C2)
#ciper text = (C1.C2)
#calculate K = C1^XA mod q
#plain text M=(c2*k^-1) mod q

def decrept_gamal(messagecopy,XA):
    #{q, a, YA, XA}
    print("======================================================>start decryption")
    #print("coming messagecopy=",messagecopy)
    #
    tempmessage = messagecopy.split(",")

    C1 = int(tempmessage[0])
    q=int(tempmessage[-1])
    C2=[]
    for i in range(len(tempmessage)):
        if i!=0 and i!=len(tempmessage)-1:
            C2.append(int(tempmessage[i]))

    print("tempmessage after spliting",tempmessage)
    #print("full message=", messagecopy)
    print("Ban ma y= (y1,y2) = (", C1, ",",C2,")")

    temp = C1 ** XA
    K = temp % q
    # print("K = ", K)
    kinverse = K
    ct = 1

    # thuật toán tính nghịch đảo của k bằng pp vét cạn Casio
    while ((kinverse * ct) % q != 1):
        ct += 1

    kinverse = ct
    print("tim nghich dao cua K = ", kinverse)
    # tạo ra mảng giải mã theo bảng mã ascii
    output = []
    for i in range(len(C2)):
        temp = C2[i] * kinverse
        letter = temp % q
        output.append(letter)

    print("Ket qua tra ve theo bang ma ascii: ", output)
    # tạo ra mảng giải mã theo bảng chữ cái
    decryptedText = ""
    for i in range(len(output)):
        temp = chr(output[i])
        decryptedText = decryptedText + temp
        # decryptedText.append(temp)

    print("Giai ma ra: ", decryptedText)

    return decryptedText