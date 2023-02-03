'''Создайте программу для игры с конфетами человек против человека.

Условие задачи: На столе лежит 202 конфета. Играют два игрока делая ход друг после друга.
Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет.
Все конфеты оппонента достаются сделавшему последний ход. Сколько конфет нужно взять первому игроку,
чтобы забрать все конфеты у своего конкурента?

a) Добавьте игру против бота
b) Подумайте как наделить бота ""интеллектом""'''

import random

bank = 202

candies = {}
candies['1'], candies['2'] = 0, 0


def make_a_move(player):                  #совершить ход
    global bank

    print(f'>>>Очередь игрока {player}')

    opponent = '1' if player == '2' else '2'
    print(f'У игрока {player} - {candies[player]} конфет | У игрока {opponent} - {candies[opponent]} конфет.')
    print(f'На столе осталось {bank} конфет')

    while True:
        number_candies = int(input('Сколько конфет забрать?:'))
        if number_candies > bank:
            print('Недостаточно конфет на столе')
            continue
        elif number_candies > 28:
            print(f'Можно взять не более 28 конфет')
            continue
        else:
            break

    candies[player] += number_candies
    bank -= number_candies


def switch_turn():              #перевести очередь на другого игрока
    global player

    if player == '1':
        player = '2'
    else:
        player = '1'


def win_check(player):                #проверить, выиграл ли игрок
    global bank

    opponent = '1' if player == '2' else '2'

    if bank == 0:
        candies[player] += candies[opponent]
        candies[opponent] = 0
        print(f'Игрок {player} выиграл! \nУ игрока {player} - {candies[player]} конфет. '
              f'У игрока {opponent} - {candies[opponent]} конфет.')


'''Идея решения: выигрывает тот игрок, кто успевает перехватить "инициативу".
Под инициативой имеется в виду возможность совершать такие ходы, которые независимо от ходов
оппонента приведут к выигрышу.
Можно использовать следующую стратегию: дополнять ходы оппонента до суммы 29 конфет.
То есть, какое бы кол-во конфет ни взял оппонент, общая сумма хода должна быть равнв 29.
Например, 10 - 19, 15 - 14, 28 - 1 и т.д.
Следовательно, задача 1-го игрока в первый ход взять стоько конфет, чтобы на столе
осталось число, кратное 29. И далее, дополняя каждый ход оппонента до 29, довести игру до конца и выиграть.
'''


player = random.choice(['1', '2'])        #жеребьевка для 1-го хода
print(f'Добро пожаловать в игру! Первым ходит {player} игрок.')
print(f'Игроку, кот. первый совершает ход, нужно взять {bank % 29} конфет, чтобы выиграть')

while bank > 0:
    make_a_move(player)
    win_check(player)
    switch_turn()


'''
Игра против бота (Эту часть можно запускать отдельно :) )
'''

import random

bank = 202

candies = {}
candies['You'], candies['Bot'] = 0, 0

def input_number():

    while True:
        number_candies = int(input('Сколько конфет забрать?:'))
        if number_candies > bank:
            print('Недостаточно конфет на столе')
            continue
        elif number_candies > 28:
            print(f'Можно взять не более 28 конфет')
            continue
        else:
            break

    return number_candies


def make_a_move_bot(player, who_is_first, first_move):         #сделать ход
    global bank
    global your_right_move
    global num_you
    global second_move

    if who_is_first == 'Bot':                              #если первым ходит Bot

        if player == 'Bot' and first_move:                 #если это первый ход Bot
            print(f'>>>Bot сделал свой ход.')
            opponent = 'You'
            number_candies = bank % 29
            print(f'Bot взял {number_candies} конфет.')

        elif player == 'Bot' and not first_move:           #если это не первый ход Bot
            print(f'>>>Bot сделал свой ход.')
            opponent = 'You'
            number_candies = 29 - num_you
            print(f'Bot взял {number_candies} конфет.')

        elif player == 'You':                              #если сейчас очередь игрока
            print(f'>>>Ваша очередь:')
            opponent = 'Bot'
            number_candies = input_number()
            num_you = number_candies

    elif who_is_first == 'You':                             #если первым ходит игрок

        if player == 'You' and first_move:                  #если это первый ход игрока
            print(f'>>>Ваша очередь:')
            print(f'Игроку, кот. первый совершает ход, нужно взять {bank % 29} конфет, чтобы выиграть')
            print(f'На столе {bank} конфет.')
            opponent = 'Bot'
            number_candies = input_number()
            num_you = number_candies

            if number_candies == bank % 29:
                your_right_move = True
            else:
                your_right_move = False

        elif player == 'You' and not first_move:            #если это не первый ход игрока
            print(f'>>>Ваша очередь:')
            opponent = 'Bot'
            number_candies = input_number()
            num_you = number_candies

        elif player == 'Bot' and your_right_move:        #если это ход Bot, и игрок сделал верный ход согласно стратегии
            print(f'>>>Bot сделал свой ход.')
            opponent = 'You'
            number_candies = min(random.randint(1, 28), bank)
            print(f'Bot взял {number_candies} конфет.')

        elif player == 'Bot' and not your_right_move:     #если это ход Bot, и игрок сделал неверный ход согласно стратегии
            print(f'>>>Bot сделал свой ход.')
            opponent = 'You'

            if second_move:                               #если это второй ход Bot
                if num_you < rest:
                    number_candies = min(rest - num_you, bank)
                else:
                    number_candies = min(29 - (num_you - rest), bank)
                second_move = False
            else:                                         #если это не второй ход Bot
                number_candies = 29 - num_you

            print(f'Bot взял {number_candies} конфет.')

    candies[player] += number_candies
    bank -= number_candies

    print(f'У игрока {player} - {candies[player]} конфет | У игрока {opponent} - {candies[opponent]} конфет.')
    print(f'На столе осталось {bank} конфет')


def win_check_bot(player):                #проверить, выиграл ли игрок
    global bank

    opponent = 'Bot' if player == 'You' else 'You'

    if bank == 0:
        candies[player] += candies[opponent]
        candies[opponent] = 0
        print(f'Игрок {player} выиграл! \nУ игрока {player} - {candies[player]} конфет. '
              f'У игрока {opponent} - {candies[opponent]} конфет.')


def switch_turn_bot():              #перевести очередь на другого игрока
    global player

    if player == 'You':
        player = 'Bot'
    else:
        player = 'You'


who_is_first = random.choice(['You', 'Bot'])        #жеребьевка для 1-го хода
print(f'Добро пожаловать в игру! Первым ходит {who_is_first}.')
player = who_is_first
first_move = True            #переменная, чтобы проверить номер хода игроков (первый или последущий за ним)
your_right_move = False      #переменная, чтобы запомнить выигрышный ли был предыдущий ход оппонента
second_move = True           #переменная, чтобы проверить номер хода бота (второй или последущий за ним)
num_you = 0                  #переменная, чтобы запомнить предыдущий ход оппонента
rest = bank % 29


while bank > 0:

    make_a_move_bot(player, who_is_first, first_move)
    win_check_bot(player)
    switch_turn_bot()

    first_move = False