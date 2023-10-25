from secrets import randbelow
from random import randint, seed
from time import sleep

from config import ID_BOB, ID_ALICE
from mqtt import MQTT
from ui import UI


def get_m() -> int:
    m: int = None
    while m is None or m < 0:
        try:
            m: int = int(
                input('Introduce the size (bits) of the b sequence: '))
            if m <= 0:
                print('Introduce a number greater than 0!')
        except ValueError:
            continue
    return m


def get_b(m: int) -> tuple[int]:
    b: list[int] = []
    for i in range(m):
        b_i: int = None
        while b_i not in {0, 1}:
            try:
                b_i = int(input(f'Introduce the bit b{i+1}: '))
            except ValueError:
                continue
        b.append(b_i)
    return tuple(b)


def G(s: tuple[int], length: int) -> tuple[int]:
    seed(bytes(s))
    return tuple(randint(0, 1) for _ in range(length))


def Gr(g: tuple[int], r: tuple[int], reverse: bool = False) -> tuple[int]:
    if reverse:
        r = tuple(not i for i in r)
    return tuple(i for i, j in zip(g, r) if j)


def get_e(c: tuple[int], gr: tuple[int]) -> tuple[int]:
    return tuple(i ^ j for i, j in zip(c, gr))


def __send_message(mqtt: MQTT, id: str, name: str, value):
    UI.set_faint()
    print('Activating node...', end=' ')
    mqtt.connect()
    print('Done')
    UI.reset_style()

    print(f'Sending {name}...', end=' ')
    mqtt.publish(id, value)
    print('Done')


def __receive_message(mqtt: MQTT):
    UI.set_faint()
    print('Activating node...', end=' ')
    mqtt.connect()
    mqtt.loop_forever()
    UI.reset_style()


def commit_stage() -> dict:
    mqtt: MQTT = MQTT(ID_ALICE)

    UI.set_bold()
    m: int = get_m()
    b: tuple[int] = get_b(m)
    UI.reset_style()

    # Fix n = 3m
    n: int = 3*m

    # Let Bob know about m
    __send_message(mqtt, ID_BOB, 'm', m)

    # Bob generates a random vector
    r: tuple[int] = None
    print('Waiting for r...')
    try:
        __receive_message(mqtt)
        r: str = mqtt.payload.decode('ascii').strip('()').split(',')
        r: tuple[int] = tuple(int(i) for i in r)
        mqtt.payload = None
    except ValueError:
        print(UI.error('Error casting r!'))
        UI.reset_style()
        exit(-1)

    # Alice forms c = (b, b, b)
    c = b*3

    # Alice selects a seed s ∈ {0, 1}^n
    s: tuple[int] = tuple(randbelow(2) for _ in range(n))
    g = G(s, len(r))

    # Alice sends e = c ⊕ Gr(s) to Bob
    gr: tuple[int] = Gr(g, r)
    e: tuple[int] = get_e(c, gr)
    sleep(2)
    __send_message(mqtt, ID_BOB, 'e', str(e))

    # Also, for each 1≤i≤2q such that ri = 0, Alice sends the i-th bit of G(s)
    gt: tuple[int] = Gr(g, r, reverse=True)
    sleep(2)
    __send_message(mqtt, ID_BOB, 'gt', str(gt))

    return {
        'm': m,
        'n': n,
        'b': b,
        's': s,
        'r': r,
        'g': g,
        'gr': gr,
        'gt': gt,
        'c': c,
        'e': e,
    }


def prove_and_verify_stage(data: dict):
    mqtt: MQTT = MQTT(ID_ALICE)

    # Alice sends (s, b1, ... , bm) to Bob
    sleep(2)
    __send_message(mqtt, ID_BOB, '(s, b)', str(data['s'] + data['b']))


if __name__ == "__main__":
    try:
        print(UI.header('BEGIN OF COMMIT STAGE'))
        data: dict = commit_stage()
        print(UI.header('END OF COMMIT STAGE'))

        print(UI.cyan('DATA:'))
        for k, v in data.items():
            print(UI.cyan(f'· {k}: {v}'))

        print(UI.header('BEGIN OF PROVE AND VERIFY STAGE'))
        prove_and_verify_stage(data)
        print(UI.header('END OF PROVE AND VERIFY STAGE'))
    except KeyboardInterrupt:
        print()
        UI.reset_style()
        print('Exiting...')

    UI.reset_style()
