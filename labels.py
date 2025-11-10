from fpdf import FPDF
import qrcode
import subprocess
import os


def start_label(labelx, labely, orientation='portrait'):
    pdf = FPDF(orientation, format=(labelx, labely))
    pdf.set_margin(0)
    pdf.add_font(family="Segou UI", fname="segoeui.ttf")

    pdf.add_page()

    return pdf


def get_printer(labelx, labely):
    label_size = str(labelx) + "x" + str(labely)
    printer = os.environ.get('PRINTER_'+label_size, os.environ.get('PRINTER_DEFAULT'))
    print("Using printer: ", printer)
    return printer


def finish_label(pdf, printer):
    # TODO tmpfile
    pdf.output("output.pdf")

    print("Printing label:")
    command = "lp -d " + printer + " output.pdf"
    print(command)
    result = subprocess.run(command,
                            shell=True,
                            capture_output=True,
                            text=True)
    print(result.stdout)
    print(result.stderr)


# Item
def item(data):
    labelx = 25
    labely = 25
    pdf = start_label(labelx, labely)
    pdf.set_font('Segou UI', size=6)

    # code = "INV-ABCDEFGHIJKL"
    code = data["id"]
    img = qrcode.make(code, border=0)
    qrsize = 17
    pdf.image(img.get_image(), x=((labelx-qrsize)/2), y=2.5, w=qrsize)

    pdf.set_y(qrsize+2.5+1)
    pdf.cell(text=code, center=True, align="C")

    printer = get_printer(labelx, labely)
    finish_label(pdf, printer)

