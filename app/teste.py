decimal = 3.40

decimal_string  = str(decimal)

dot_check = False
integer_list = []
decimal_list = []
for caractere in decimal_string:
    if caractere == '.':
        dot_check = True
        continue
    if dot_check == False:
        integer_list.append(caractere)
    else:
        decimal_list.append(caractere)

minutes = str(round(float(f'0.{"".join(decimal_list)}') * 60))

return (f'{"".join(integer_list)}:{minutes}')