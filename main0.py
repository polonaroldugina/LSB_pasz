from PIL import Image
import binascii
import math


def bits1(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))




def alignment(bin_num, target_len):
    cur_len = len(bin_num)
    if cur_len < target_len:
        return f'{"0"*(target_len-cur_len)}{bin_num}'
    else:
        return bin_num

def bits2(text):
    with open(text, mode="rb") as pbmfl:
        br = pbmfl.read()
    bin_data = [alignment(f'{bs:b}', 8) for bs in list(br)]
    ans = ''.join(bin_data)
    return ans
    


#Всраивание сообщения в изображение


x = int(input('Введите 1 - если на входит поступит битовая последовательность, 2 - текст, 3 - изображение, 4 - необходимо извлечь текст из картинки:  '))
if x == 1:
    text = input('Введите сообщение в двоичной форме(допустимы символы: 0,1). Сообщение: ')
   
if x == 2:
    text = input('Сообщение: ')
    text = bits1(text)
    
if x == 3:
    text = input('Название файла: ')
    text = bits2(text)
    
if x != 4:
    im = Image.open('cat.jpg')
    n, m = im.size
    print('Максимальная длина', n * m * 7 - 16)
    ss = 0
    pix = im.load()
    n, m = im.size
    v = len(text)
    dlina = bin(v)[2:]
    dl0 = len(dlina)
    while dl0 != 16 :
        dl0 = len(dlina)
        if dl0 > 16:
            print('Внимание, под размер сообщения выделено больше бит, чем по умолчанию! Их число',(len(dlina)))
            dl0 = 16
        else:
            dlina = '0' + dlina
        
    print('Длина вашего сообщения с учетом места под длину', len(dlina)+ len(text))
    k = 0
    text = str(dlina) + text
    for x in range(n):
        for y in range(m):
            r, g, b = pix[x,y]
            s0 = 0.3 * r + 0.59 * g +0.11 * b
        
            r = bin(r)[2:]
            g = bin(g)[2:]
            b = bin(b)[2:]
        
            if len(text) >= 7 and len(str(r)) > 7:
                s = text[:7]
                if int(r[-1]) != int(s[0]):
                    k += 1
                if int(r[-2]) != int(s[1]):
                    k += 4
                r = int(r[:-7] + s)
                text = text[7:]
        
            if len(text) >= 7 and len(str(g)) > 7:
                s = text[:5]
                if int(g[-1]) != int(s[0]):
                    k += 1
                if int(g[-2]) != int(s[1]):
                    k += 1
                r = int(g[:-7] + s)
                text = text[7:]
        
            if len(text) >= 7 and len(str(b)) > 7:
                s = text[:7]
                if int(b[-1]) != int(s[0]):
                    k += 1
                if int(b[-2]) != int(s[1]):
                    k += 2
                r = int(b[:-7] + s)
                text = text[7:]

                
            pix[x,y] = int(str(r), base=2), int(str(g), base=2), int(str(b), base=2)
            s1 = 0.3 * int(str(r), base=2)+ 0.59 * int(str(g), base=2)+ 0.11 * int(str(b), base=2)
        
            ss += (s1 - s0)*(s1 - s0)
        #print(x)
        

  
    im.save('cat0.png')
    print('Расчет показателей встраивания: ')
    print('EC (количеств бит на пиксель) =', v /(m * n))
    mse = ss / (m * n)
    
    print('PSNR (пиковое отношение сигнал - шум) =', 10 * math.log10((255*255)/(mse)))
    print('BER (интенсивность битовых ошибок) =', k / v)
    
elif x == 4:
    text = input('Введите название изображения: ')
    im = Image.open(text)
    n, m = im.size
    pix = im.load()
    ans = ''
  
    for x in range(n):
        for y in range(m):
            r, g, b = pix[x,y]
            r = bin(r)[2:]
            g = bin(g)[2:]
            b = bin(b)[2:]
            ans = ans + str(r[-1])+str(g[-1])+str(b[-1])
    dlina = ans[:16]

    dlina = int(str(dlina), base=2)
    print(dlina)
    ans = ans[16:]
    ans = ans[:dlina]
    print(dlina, len(ans))
    print('Расшифрованная последовательность: ', ans)
        
        
