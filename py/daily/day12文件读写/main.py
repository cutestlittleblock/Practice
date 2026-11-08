f=open("test.txt","a",encoding="utf-8")
f.write("你好世界")


f=open("test.txt","r",encoding="utf-8")
contant=f.read()

print(contant)