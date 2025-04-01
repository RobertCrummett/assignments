spacing = 12.5
with open("gravity-data.txt") as file, open("profile.txt", "w") as fout:
    for i, line in enumerate(file):
        fout.write(f"{spacing * i} " + line)
