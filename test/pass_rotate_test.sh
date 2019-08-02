#!/usr/bin/env bats

load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

TMPDIR=""

setup() {
    filename="$(basename "$BATS_TEST_FILENAME" ".sh")"
    TMPDIR="$(mktemp -d -p "$BATS_TMPDIR" "$filename.XXXXXX")"
    export XDG_CONFIG_HOME="$TMPDIR"
}

teardown() {
    [[ -z "$TMPDIR" ]] && rm -rf "$TMPDIR"
    unset XDG_CONFIG_HOME
}

@test "Able to lookup account" {
    echo pass > "$TMPDIR/test-noop"

    cat <<EOF > "$TMPDIR/pass-rotate.ini"
[pass-rotate]
get-password=cat "$TMPDIR/test-\$ACCOUNT"
gen-password=echo new-pass | tee "$TMPDIR/test-\$ACCOUNT"
[noop]
username=pg
cassette=$TMPDIR/cassette
EOF

    run $BATS_TEST_DIRNAME/../pass-rotate noop
    assert_success
    assert_line 'Rotating noop... OK'

    run cat "$TMPDIR/test-noop"
    assert_output 'new-pass'

    run cat "$TMPDIR/cassette"
    assert_output <<'EOF'
prepare pg: pass
execute pg: pass new-pass
EOF
}

@test "Able to rotate password with set-password" {
    echo pass > "$TMPDIR/test-noop"

    cat <<EOF > "$TMPDIR/pass-rotate.ini"
[pass-rotate]
get-password=cat "$TMPDIR/test-\$ACCOUNT"
set-password=tee "$TMPDIR/test-\$ACCOUNT"
gen-password=echo "new-pass"
[noop]
username=pg
cassette=$TMPDIR/cassette
EOF

    run $BATS_TEST_DIRNAME/../pass-rotate noop
    assert_success
    assert_line 'Rotating noop... OK'

    run cat "$TMPDIR/test-noop"
    assert_output 'new-pass'

    run cat "$TMPDIR/cassette"
    assert_output <<'EOF'
prepare pg: pass
execute pg: pass new-pass
EOF
}

@test "Able to use get-account" {
    echo pass > "$TMPDIR/test-noop"

    cat <<EOF > "$TMPDIR/pass-rotate.ini"
[pass-rotate]
get-account=echo '{ "password": "'\$(cat "$TMPDIR/test-noop")'", "username": "pg" }'
set-password=tee "$TMPDIR/test-\$ACCOUNT"
gen-password=echo "new-pass"

[noop]
cassette=$TMPDIR/cassette
EOF

    run $BATS_TEST_DIRNAME/../pass-rotate noop
    assert_success
    assert_line 'Rotating noop... OK'

    run cat "$TMPDIR/test-noop"
    assert_output new-pass

    run cat "$TMPDIR/cassette"
    cat <<'EOF' | assert_output
prepare pg: pass
execute pg: pass new-pass
EOF
}
