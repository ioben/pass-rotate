import textwrap
from passrotate.parsers.password_store import parse

def test_no_password():
    assert actual("") == expected("")
    assert actual("\n") == expected("")

def test_just_password():
    assert actual("password") == expected("password")
    assert actual(" password ") == expected(" password ")
    assert actual("\t./..,!@#$^&()\t") == expected("\t./..,!@#$^&()\t")

def test_password_and_attributes():
    assert actual("""\
        p
        user: blah
        url: blah.com
        """) == expected("p", { "user": "blah", "url": "blah.com" })

    assert actual("""\
        p

        user: blah
        url: blah.com
        """) == expected("p", { "user": "blah", "url": "blah.com" })

    assert actual("""\
        p

        url: blah.com
        """) == expected("p", { "url": "blah.com" })


def test_password_attributes_and_description():
    assert actual("""\
        p

        url: blah.com

        """) == expected("p", { "url": "blah.com" })

    assert actual("""\
        p
        user: blah
        url: blah.com

        line1
        """) == expected("p", { "user": "blah", "url": "blah.com" }, "line1")

    assert actual("""\
        p

        user: blah
        url: blah.com

        line1
        line2
        """) == expected("p", { "user": "blah", "url": "blah.com" }, "line1\nline2")

    assert actual("""\
        p

        user: blah
        url: blah.com

        line1
        line2


        """) == expected("p", { "user": "blah", "url": "blah.com" }, "line1\nline2")

def actual(raw):
    if len(raw.strip().splitlines()) == 1:
        return parse(raw.splitlines())
    else:
        return parse(textwrap.dedent(raw).splitlines(True))

def expected(password, attributes={}, description=""):
    return {
        "password": password,
        **attributes,
        "description": description,
    }
