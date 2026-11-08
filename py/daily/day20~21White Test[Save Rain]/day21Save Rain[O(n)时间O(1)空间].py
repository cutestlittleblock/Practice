pillar=[]
rain=0
given_pillar=input("请给定柱子,数字间用“,”隔开:")

n_str=given_pillar.split(",")
for n in n_str:
    pillar.append(int(n))

l=0
r=len(pillar)-1
left_max=pillar[0]
right_max=pillar[-1]

while l<r:
    if left_max<right_max:
        l+=1
        left_max=max(left_max,pillar[l])
        rain+=left_max-pillar[l]
    else:
        r-=1
        right_max=max(right_max,pillar[r])
        rain+=right_max-pillar[r]

print(rain)