def parse(lines):
    lines = "".join(lines).splitlines()

    password = ""
    attributes = {}
    description_lines = []

    state = "password"

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()

        # Password must be first line
        if state == "password":
            password = raw_line
            state = "after-password"

        # Read K/V pairs separated by a colon
        elif state in ["after-password", "attributes"]:
            if state == "after-password":
                state = "attributes"
                if not line:
                    continue

            if line:
                key, value = line.split(':', 1)
                attributes[key.strip()] = value.strip()
            else:
                state = "description"

        elif state == "description":
            description_lines.append(line)

        else:
            raise Exception("Reached invalid state " + state + ", line: " + str(i + 1))

    return {
        "password": password,
        **attributes,
        "description": "\n".join(description_lines).strip(),
    }
