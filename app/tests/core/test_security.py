from datetime import datetime, timedelta
from unittest import mock

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    create_jwt_token,
    decode_jwt_token,
    get_password_hash,
    verify_password,
)

# region function get_password_hash


def test_when_get_password_hash_must_return_a_str():
    hash_ = get_password_hash("testing_password")
    assert isinstance(hash_, str)


def test_when_get_password_hash_must_return_a_hash_with_60_characters():
    hash_ = get_password_hash("testing_password")
    assert len(hash_) == 60


def test_when_get_password_hash_must_return_a_hash():
    password = "testing_password"
    hash_ = get_password_hash(password)
    assert hash_ != password


def test_when_get_password_hash_of_the_same_password_must_return_different_hashes():
    # testing hash salt concept.
    password = "testing_password"
    hash_1 = get_password_hash(password)
    hash_2 = get_password_hash(password)
    assert hash_1 != hash_2


# endregion

# region function verify_password


def test_when_verify_password_must_return_a_bool():
    password = "testing_verify_password"
    hash_ = get_password_hash(password)
    result = verify_password(password, hash_)
    assert isinstance(result, bool)


def test_when_verify_password_if_password_and_hash_are_correct_must_return_true():
    password = "testing_verify_password"
    hash_ = get_password_hash(password)
    result = verify_password(password, hash_)
    assert result is True


def test_when_verify_password_if_password_and_hash_are_incorrect_must_return_false():
    hash_ = get_password_hash("testing_verify_password")
    result = verify_password("incorrect_password", hash_)
    assert result is False


# endregion

# region function decode_jwt_token


def test_when_decode_jwt_token_must_return_a_dict():
    jwt_token = create_jwt_token(subject="test_decode")
    jwt_payload = decode_jwt_token(jwt_token)
    assert isinstance(jwt_payload, dict)


def test_when_decode_jwt_token_must_return_have_sub_key():
    jwt_token = create_jwt_token(subject="test_decode")
    jwt_payload = decode_jwt_token(jwt_token)
    assert "sub" in jwt_payload


def test_when_decode_jwt_token_must_return_have_exp_key():
    jwt_token = create_jwt_token(subject="test_decode")
    jwt_payload = decode_jwt_token(jwt_token)
    assert "exp" in jwt_payload


def test_when_decode_jwt_token_must_return_the_same_subject_used_in_jwt_token():
    subject = "test_decode"
    jwt_token = create_jwt_token(subject=subject)
    jwt_payload = decode_jwt_token(jwt_token)
    assert jwt_payload["sub"] == subject


def test_when_decode_jwt_token_must_return_have_nbf_key():
    jwt_token = create_jwt_token(subject="test_decode")
    jwt_payload = decode_jwt_token(jwt_token)
    assert "nbf" in jwt_payload


def test_when_decode_jwt_token_if_token_is_expired_it_must_raise_expired_signature_error():
    negative_expires_delta = timedelta(minutes=-5)
    jwt_token = create_jwt_token(
        subject="test_decode", expires_delta=negative_expires_delta
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_jwt_token(jwt_token)


def test_when_decode_jwt_token_if_token_is_not_valid_yet_it_must_raise_immature_signature_error():
    positive_starts_delta = timedelta(minutes=10)
    jwt_token = create_jwt_token(
        subject="test_decode", starts_delta=positive_starts_delta
    )
    with pytest.raises(jwt.ImmatureSignatureError):
        decode_jwt_token(jwt_token)


def test_when_decode_jwt_token_if_token_is_invalid_it_must_raise_invalid_token_error():
    with pytest.raises(jwt.InvalidTokenError):
        decode_jwt_token("invalid_token")


# endregion

# region create_jwt_token


def test_when_create_jwt_token_must_return_a_str():
    subject = "testing"
    jwt_token = create_jwt_token(subject)
    assert isinstance(jwt_token, str)


# I'm mocking datetime to datetime.utcnow function return
# the same time that I'm using in the test.
@mock.patch("app.core.security.datetime")
def test_when_create_jwt_token_if_starts_delta_was_passed_the_nbf_must_be_uct_now_plus_starts_delta(
    mocked_datetime,
):
    # replacing microsecond because pyjwt convert the datetime to
    # timestamp lost the microseconds
    test_utc_now = datetime.utcnow().replace(microsecond=0)
    mocked_datetime.utcnow.return_value = test_utc_now

    # using start_delta negative because decode_jwt_token will check the nbf
    # and if the current time is greater than the nbf it will raise an exception.
    starts_delta = timedelta(minutes=-10)
    jwt_token = create_jwt_token(
        subject="test_decode", starts_delta=starts_delta
    )
    jwt_payload = decode_jwt_token(jwt_token)

    expected = test_utc_now + starts_delta
    result = datetime.utcfromtimestamp(jwt_payload["nbf"])
    assert result == expected


@mock.patch("app.core.security.datetime")
def test_when_create_jwt_token_if_starts_delta_was_not_passed_the_nbf_must_be_uct_now_plus(
    mocked_datetime,
):
    # replacing microsecond because pyjwt convert the datetime to
    # timestamp and lost the microseconds
    test_utc_now = datetime.utcnow().replace(microsecond=0)
    mocked_datetime.utcnow.return_value = test_utc_now

    jwt_token = create_jwt_token(subject="test_decode")
    jwt_payload = decode_jwt_token(jwt_token)

    result = datetime.utcfromtimestamp(jwt_payload["nbf"])
    assert result == test_utc_now


@mock.patch("app.core.security.datetime")
def test_when_create_jwt_token_if_expires_delta_was_passed_the_exp_must_be_uct_now_plus_expires_delta(
    mocked_datetime,
):
    # replacing microsecond because pyjwt convert the datetime to
    # timestamp and lost the microseconds
    test_utc_now = datetime.utcnow().replace(microsecond=0)
    mocked_datetime.utcnow.return_value = test_utc_now

    expires_delta = timedelta(minutes=5)
    jwt_token = create_jwt_token(
        subject="test_decode", expires_delta=expires_delta
    )
    jwt_payload = decode_jwt_token(jwt_token)

    expected = test_utc_now + expires_delta
    result = datetime.utcfromtimestamp(jwt_payload["exp"])
    assert result == expected


@mock.patch("app.core.security.datetime")
def test_when_create_jwt_token_if_expires_delta_was_not_passed_the_exp_must_be_uct_now_plus_config_token_expires_minutes(
    mocked_datetime,
):
    # replacing microsecond because pyjwt convert the datetime to
    # timestamp and lost the microseconds
    test_utc_now = datetime.utcnow().replace(microsecond=0)
    mocked_datetime.utcnow.return_value = test_utc_now

    jwt_token = create_jwt_token(subject="test_decode")
    jwt_payload = decode_jwt_token(jwt_token)

    expected = test_utc_now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    result = datetime.utcfromtimestamp(jwt_payload["exp"])
    assert result == expected


# endregion
