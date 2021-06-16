import pytest

import fixed_width

def test_default_int8_t_to_int() -> None:
    from fixed_width import u8

    assert int(u8(1)) == 1
    assert int(u8(16)) == 16
    assert int(u8(128)) == 128


def test_default_to_int_overflow() -> None:
    from fixed_width import u8

    assert int(u8(256)) == 0
    assert int(u8(257)) == 1


def test_c_stdint_int8_t_to_int() -> None:
    assert int(fixed_width.c_stdint.int8_t(1)) == 1
    assert int(fixed_width.c_stdint.int8_t(16)) == 16
    assert int(fixed_width.c_stdint.int8_t(128)) == 128


def test_c_stdint_uint8_t_to_int() -> None:
    assert int(fixed_width.c_stdint.uint8_t(1)) == 1
    assert int(fixed_width.c_stdint.uint8_t(16)) == 16
    assert int(fixed_width.c_stdint.uint8_t(128)) == 128
    assert int(fixed_width.c_stdint.uint8_t(255)) == 255


def test_c_stdint_uint8_t_to_int_with_context() -> None:
    with fixed_width.c_stdint() as ctx:
        assert int(ctx.uint8_t(1)) == 1
        assert int(ctx.uint8_t(16)) == 16
        assert int(ctx.uint8_t(128)) == 128
        assert int(ctx.uint8_t(255)) == 255

        assert ctx.overflow == False
        assert ctx.promotion == False


def test_c_stdint_uint8_t_to_int_overflow() -> None:
    assert int(fixed_width.c_stdint.uint8_t(256)) == 0
    assert int(fixed_width.c_stdint.uint8_t(257)) == 1


def test_c_stdint_uint8_t_to_int_overflow_with_context() -> None:
    with fixed_width.c_stdint() as ctx:
        assert int(fixed_width.c_stdint.uint8_t(256)) == 0

        assert ctx.overflow == True
        assert ctx.promotion == False

    with fixed_width.c_stdint() as ctx:
        assert int(fixed_width.c_stdint.uint8_t(257)) == 1

        assert ctx.overflow == True
        assert ctx.promotion == False


def test_c_stdint_uint16_t_to_int() -> None:
    assert int(fixed_width.c_stdint.uint16_t(1)) == 1
    assert int(fixed_width.c_stdint.uint16_t(16)) == 16
    assert int(fixed_width.c_stdint.uint16_t(128)) == 128
    assert int(fixed_width.c_stdint.uint16_t(256)) == 256
    assert int(fixed_width.c_stdint.uint16_t(65_535)) == 65_535


def test_c_stdint_uint16_t_to_int_overflow() -> None:
    assert int(fixed_width.c_stdint.uint16_t(65_536)) == 0
    assert int(fixed_width.c_stdint.uint16_t(65_537)) == 1


def test_c_stdint_uint32_t_to_int() -> None:
    assert int(fixed_width.c_stdint.uint32_t(1)) == 1
    assert int(fixed_width.c_stdint.uint32_t(16)) == 16
    assert int(fixed_width.c_stdint.uint32_t(128)) == 128
    assert int(fixed_width.c_stdint.uint32_t(256)) == 256
    assert int(fixed_width.c_stdint.uint32_t(4_294_967_295)) == 4_294_967_295


def test_c_stdint_uint32_t_to_int_overflow() -> None:
    assert int(fixed_width.c_stdint.uint32_t(4_294_967_296)) == 0
    assert int(fixed_width.c_stdint.uint32_t(4_294_967_297)) == 1


def test_c_stdint_uint64_t_to_int() -> None:
    assert int(fixed_width.c_stdint.uint64_t(1)) == 1
    assert int(fixed_width.c_stdint.uint64_t(16)) == 16
    assert int(fixed_width.c_stdint.uint64_t(128)) == 128
    assert int(fixed_width.c_stdint.uint64_t(256)) == 256

    assert (
        int(fixed_width.c_stdint.uint64_t(18_446_744_073_709_551_615))
        == 18_446_744_073_709_551_615
    )


def test_c_stdint_uint64_t_to_int_overflow() -> None:
    assert int(fixed_width.c_stdint.uint64_t(18_446_744_073_709_551_616)) == 0
    assert int(fixed_width.c_stdint.uint64_t(18_446_744_073_709_551_617)) == 1
