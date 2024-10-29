import uuid

with open("uuids.txt", "a") as output_file:
    output_file.write("\n")
    output_file.write("Images\n")
    for i in range(3):
        output_file.write(f"Folder {i+1}\n")
        for j in range(2):
            output_file.write(str(uuid.uuid4()))
            output_file.write("\n")
