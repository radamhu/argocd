is_old = False
is_licensed = False

if is_old:
    print('You are old engough to drive')
elif is_licensed:
    print('ypu can drive now')
else:
    print('you are not of age')

print('okoko')

is_friend = True

can_message = "message allow" if is_friend else "not allowed message"

print(can_message)

is_magician = True
is_expert = False

if is_expert and is_magician:
    print('you are a mster magician')
elif is_magician and not is_expert:
    print('at least youare getting there')
elif not is_magician:
    print('you need magic power')

print(True == 1)
print('' == 1)
print([] == 1)
print(10 == 10.0)
print([] == [])