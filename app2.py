import os
import time
import glob
from flask import Flask, redirect, render_template, request, send_file
from huffman_coding import huffman_compress_file, huffman_decompress_file  # Import your Huffman coding functions


# Configure Application
app = Flask(__name__)

global filename
global ftype

@app.route("/")
def home():

    # Delete old files
    filelist = glob.glob('uploads/*')
    for f in filelist:
        os.remove(f)
    filelist = glob.glob('downloads/*')
    for f in filelist:
        os.remove(f)
    return render_template("home.html")

app.config["FILE_UPLOADS"] = "uploads"


def huffman_compress(file_path):
    compressed_file_path = os.path.join(app.config["FILE_UPLOADS"], filename + "-compressed.bin")
    huffman_compress_file(file_path, compressed_file_path)
    return compressed_file_path

def huffman_decompress(file_path):
    decompressed_file_path = os.path.join(app.config["FILE_UPLOADS"], filename + "-decompressed.txt")
    huffman_decompress_file(file_path, decompressed_file_path)
    return decompressed_file_path


@app.route("/compress", methods=["GET", "POST"])
def compress():

    if request.method == "GET":
        return render_template("compress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file_path = os.path.join(app.config["FILE_UPLOADS"], filename)
            up_file.save(up_file_path)

            compressed_file_path = huffman_compress(up_file_path)

            filename = filename[:filename.index(".", 1)]
            ftype = "-compressed.bin"

            while True:
                if 'uploads/{}-compressed.bin'.format(filename) in glob.glob('uploads/*-compressed.bin'):
                    os.system('mv {} downloads/'.format(compressed_file_path))
                    break

            return render_template("compress.html", check=1)

        else:
            print("ERROR")
            return render_template("compress.html", check=-1)

@app.route("/decompress", methods=["GET", "POST"])
def decompress():

    if request.method == "GET":
        return render_template("decompress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file_path = os.path.join(app.config["FILE_UPLOADS"], filename)
            up_file.save(up_file_path)

            decompressed_file_path = huffman_decompress(up_file_path)

            f = open(decompressed_file_path, 'rb')
            ftype = "-decompressed." + (f.read(int(f.read(1)))).decode("utf-8")
            filename = filename[:filename.index("-", 1)]

            while True:
                if 'uploads/{}{}'.format(filename, ftype) in glob.glob('uploads/*-decompressed.*'):
                    os.system('mv {} downloads/'.format(decompressed_file_path))
                    break

            return render_template("decompress.html", check=1)

        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)

@app.route("/download")
def download_file():
    global filename
    global ftype
    path = "downloads/" + filename + ftype
    return send_file(path, as_attachment=True)




# Restart application whenever changes are made
if __name__ == "__main__":
    app.run(debug = True)
