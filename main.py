from PIL import Image


def stegano(name_img, msg):
    im = Image.open(name_img)
    w, h = im.size
    r, g, b = im.split()
    r = list(r.getdata())
    u = len(msg)
    v = bin(len(msg))[2:].rjust(8, "0")
    ascii = [bin(ord(x))[2:].rjust(8, "0") for x in msg]
    a = ''.join(ascii)
    for j in range(8):
        r[j] = 2 * int(r[j] // 2) + int(v[j])
    for i in range(8*u):
        r[i+8] = 2 * int(r[i+8] // 2) + int(a[i])

    nr = Image.new("L", (16*w, 16*h))
    nr = Image.new("L", (w, h))
    nr.putdata(r)
    imgnew = Image.merge('RGB', (nr, g, b))
    new_name_img = "couv_" + name_img
    imgnew.save(new_name_img)


def get_msg(name_couv):
    im = Image.open(name_couv)
    r, g, b = im.split()
    r = list(r.getdata())

    # lecture de la longueur de la chaine
    p = [str(x % 2) for x in r[0:8]]
    q = "".join(p)
    q = int(q, 2)
    # lecture du message
    n = [str(x % 2) for x in r[8:8*(q+1)]]
    b = "".join(n)
    message = ""
    for k in range(0, q):
        l = b[8*k:8*k+8]
        message += chr(int(l, 2))

    return message


types = input("Voulez vous encoder ou décoder ? encoder = 1 / decoder = 0 :")
if (types == "1"):
    msg = input("Quel est le message a encoder ? : ")
    imagename = input(
        "Veuillez fournir le path de l'image a encoder (.png uniquement) : ")
    stegano(imagename, msg)
elif(types == "0"):
    imagename = input("Veuillez fournir le path de l'image a décoder : ")
    print(get_msg(imagename))
