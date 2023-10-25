from random import randint, seed
from time import sleep

from config import ID_BOB, ID_ALICE
from mqtt import MQTT
from ui import UI


def get_r(m: int, q: int) -> tuple[int]:
    r: list[int] = [0] * (2*q-1)
    while r.count(1) != q:
        i: int = randint(0, len(r)-1)
        r[i] = 1
    return tuple(r)


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
    mqtt: MQTT = MQTT(ID_BOB)

    # Receive m from Alice
    m: int = None
    print('Waiting for m...')
    try:
        __receive_message(mqtt)
        m: int = int(mqtt.payload)
        mqtt.payload = None
    except ValueError:
        print(UI.error('Error casting m!'))
        exit(-1)

    # Fix q = 3m
    q: int = 3*m

    # Bob generates a random vector r = (r1, r2, ... , r_{2q}) of bits where
    # exactly q of its bits are equal to 1
    r: tuple[int] = get_r(m, q)

    # Bob sends r to Alice
    sleep(2)
    __send_message(mqtt, ID_ALICE, 'r', str(r))

    # Receive e from Alice
    e: tuple[int] = None
    print('Waiting for e...')
    try:
        __receive_message(mqtt)
        e: str = mqtt.payload.decode('ascii').strip('()').split(',')
        e: tuple[int] = tuple(int(i) for i in e)
        mqtt.payload = None
    except ValueError:
        print(UI.error('Error casting e!'))
        UI.reset_style()
        exit(-1)

    # Receive gt from Alice
    gt: tuple[int] = None
    print('Waiting for gt...')
    try:
        __receive_message(mqtt)
        gt: str = mqtt.payload.decode('ascii').strip('()').split(',')
        gt: tuple[int] = tuple(int(i) for i in gt)
        mqtt.payload = None
    except ValueError:
        print(UI.error('Error casting gt!'))
        UI.reset_style()
        exit(-1)

    return {
        'm': m,
        'q': q,
        'r': r,
        'gt': gt,
        'e': e,
    }


def prove_and_verify_stage(data: dict):
    mqtt: MQTT = MQTT(ID_BOB)

    # Receive (s, b) from Alice
    sb: tuple[int] = None
    print('Waiting for (s, b)...')
    try:
        __receive_message(mqtt)
        sb: str = mqtt.payload.decode('ascii').strip('()').split(',')
        sb: tuple[int] = tuple(int(i) for i in sb)
        mqtt.payload = None
    except ValueError:
        print(UI.error('Error casting (s, b)!'))
        UI.reset_style()
        exit(-1)

    # len(s, b) = len(s) + len(b);
    # len(s) = n = q = 3*m;
    # len(b) = m;
    # len(s, b) = 4*m;
    print('Extracting \'s\' and \'b\'...', end=' ')
    s: tuple[int] = sb[:3*data['m']]
    b: tuple[int] = sb[3*data['m']:]
    print('Done')

    # Bob verifies for each 1≤i≤2q with ri = 0
    # that Alice sent the correct sequence
    print('Checking \'gt\'...', end=' ')
    g = G(s, len(data['r']))
    if not data['gt'] == Gr(g, data['r'], reverse=True):
        print(UI.error('Failed to check \'gt\' with \'s\'!'))
        UI.reset_style()
        exit(-2)
    print('Done')

    # Bob computes c' = (b, b, b)
    print('Computing \'c\'\'...', end=' ')
    c = b*3
    print('Done')

    # Bob verifies that e = c' ⊕ Gr(s)
    print('Verifying...', end=' ')
    if data['e'] == get_e(c, Gr(g, data['r'])):
        print(UI.success('The vector commitment was valid!'))
    else:
        print(UI.error('The vector commitment was NOT valid!'))


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
