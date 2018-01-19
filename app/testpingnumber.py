def testpingnumber(pingnumber):
    if pingnumber == "":
        return False
    try:
        int(pingnumber)
        return True
    except:
        return False
