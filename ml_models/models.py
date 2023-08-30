class ModelFiles:
    def clean(self, filename):
        f = open(filename, "wb")
        f.write(bytes("", encoding="utf-8"))
        f.close()
