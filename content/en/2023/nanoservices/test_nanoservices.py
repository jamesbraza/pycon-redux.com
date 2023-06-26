from nanoservices import moving_window_average_gen, ClearWindow, DumpData, demo
from pytest_subtests import SubTests


def test_moving_window_average(subtests: SubTests) -> None:
    with subtests.test(msg="no prefill"):
        gen = moving_window_average_gen(window_size=3)
        next(gen)
        assert gen.send(5) == 5
        assert gen.send(6) == (5 + 6) / 2
        assert gen.send(7) == (5 + 6 + 7) / 3
        assert gen.send(8) == (6 + 7 + 8) / 3
        assert gen.send(9) == (7 + 8 + 9) / 3

    with subtests.test(msg="prefill"):
        gen = moving_window_average_gen((5, 6), window_size=3)
        next(gen)
        assert gen.send(7) == (5 + 6 + 7) / 3
        assert gen.send(8) == (6 + 7 + 8) / 3
        assert gen.send(9) == (7 + 8 + 9) / 3

    with subtests.test(msg="empty data"):
        gen = moving_window_average_gen()
        next(gen)
        assert next(gen) is None

    with subtests.test(msg="invalid data"):
        gen = moving_window_average_gen()
        next(gen)
        assert gen.send("invalid") is None  # type: ignore[arg-type]

    with subtests.test(msg="clear"):
        gen = moving_window_average_gen((5, 6, 7), window_size=10)
        next(gen)
        assert gen.throw(ClearWindow) is None
        assert gen.send(8.0) == 8

    with subtests.test(msg="dump"):
        data = 5, 6, 7
        gen = moving_window_average_gen(data, window_size=10)
        next(gen)
        assert gen.throw(DumpData) == len(data)
        for value in data:
            assert next(gen) == value
        assert gen.send(8) == (5 + 6 + 7 + 8) / 4

    with subtests.test(msg="close"):
        gen = moving_window_average_gen()
        next(gen)
        gen.close()


def test_demo_runs() -> None:
    demo()
