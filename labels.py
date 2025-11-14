from fpdf import FPDF
import qrcode
import subprocess
import os


def start_label(labelx, labely, orientation='portrait'):
    pdf = FPDF(orientation, format=(labelx, labely))
    pdf.set_margin(0)
    pdf.add_font(family="Segou UI", fname="segoeui.ttf")
    pdf.add_font(family="Segou UI", fname="segoeuib.ttf", style="B")
    pdf.add_font(family="Segou UI", fname="segoeuii.ttf", style="I")
    pdf.set_font('Segou UI')

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

    if printer is None:
        print("No printer set in .env, skip printing")
        return

    print("Printing label:")
    command = "lp -d " + printer + " output.pdf"
    print(command)
    result = subprocess.run(command,
                            shell=True,
                            capture_output=True,
                            text=True)
    print(result.stdout)
    print(result.stderr)


def item_default(data):
    item_qrcode(data)


# Item QR (Dymo 30332 / S0929120)
def item_qrcode(data):
    labelx = 25
    labely = 25
    pdf = start_label(labelx, labely)
    pdf.set_font(size=6)

    code = data["id"]
    img = qrcode.make(code, border=0)
    qrsize = 17
    pdf.image(img.get_image(), x=((labelx-qrsize)/2), y=2.5, w=qrsize)

    pdf.set_y(qrsize+2.5+1)
    pdf.cell(text=code, center=True, align="C")

    printer = get_printer(labelx, labely)
    finish_label(pdf, printer)


# Location default
def location_default(data):
    location_portrait(data)


# Location QR (Dymo 30332 / S0929120)
def location_qrcode(data):
    item_qrcode(data)


# Location portrait (Dymo 99014 / S0722430)
def location_portrait(data):
    labelx = 54
    labely = 101
    pdf = start_label(labelx, labely)

    qrsize = 33

    pdf.set_y(14)
    pdf.set_font(size=68)
    pdf.cell(text=f"**{data['name']}**", markdown=True, center=True, align="C")

    x = (labelx - qrsize - 1) / 2
    pdf.set_line_width(0.4)
    pdf.line(x1=x, y1=41, x2=labelx-x, y2=41)

    pdf.set_y(45)
    pdf.set_font(size=12)
    pdf.cell(text=f"**{data['contents']}**", markdown=True, center=True, align="C")
    pdf.set_y(51)
    pdf.cell(text=f"**{data['id']}**", markdown=True, center=True, align="C")

    x = (labelx - qrsize - 1) / 2
    pdf.set_line_width(0.3)
    pdf.line(x1=x, y1=59, x2=labelx-x, y2=59)

    img = qrcode.make(data["id"], border=0)
    pdf.image(img.get_image(), x=((labelx-qrsize)/2), y=61, w=qrsize)

    printer = get_printer(labelx, labely)
    finish_label(pdf, printer)
