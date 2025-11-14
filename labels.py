from fpdf import FPDF
import qrcode
import subprocess
import os


def start_label(labelx, labely, orientation='portrait'):
    pdf = FPDF(orientation, format=(labelx, labely))
    pdf.set_auto_page_break(False)
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


# Item name (Dymo 11355 / S0722550)
def item_itemname(data):
    labelx = 19
    labely = 51
    pdf = start_label(labelx, labely, orientation='landscape')

    pdf.set_xy(5, 2)
    pdf.set_font(size=12)
    pdf.multi_cell(0, text=f"{data['name']}", markdown=True, align="L")

    printer = get_printer(labelx, labely)
    finish_label(pdf, printer)


# Item detailed (Dymo 99010 / S0722370)
def item_detailed(data):
    labelx = 28
    labely = 89
    pdf = start_label(labelx, labely, orientation='landscape')

    qrsize = 22

    pdf.set_xy(32, 5)
    pdf.set_font(size=12)
    pdf.multi_cell(0, text=f"**{data['name']}**", markdown=True, align="L")

    pdf.set_xy(32, 20)
    pdf.set_font(size=12)
    pdf.cell(text=data['id'], markdown=True, align="L")

    img = qrcode.make(data["id"], border=0)
    pdf.image(img.get_image(), x=7, y=((labelx-qrsize)/2), w=qrsize)

    printer = get_printer(labelx, labely)
    finish_label(pdf, printer)


# Item fastener (Dymo 11355 / S0722550)
def item_fastener(data):
    labelx = 19
    labely = 51
    pdf = start_label(labelx, labely)
    pdf.set_font(size=6)

    code = data["id"]
    img = qrcode.make(code, border=0)
    qrsize = 15
    with pdf.rotation(180, x=labelx/2, y=14):

        pdf.image(img.get_image(), x=((labelx-qrsize)/2), y=2.5, w=qrsize)

        pdf.set_y(19)
        pdf.set_font(size=5)
        pdf.cell(text=code, center=True, align="C")

    pdf.set_line_width(0.3)
    pdf.line(x1=2, y1=28, x2=labelx-2, y2=28)

    if "size" in data["attributes"]:
        pdf.set_y(30)
        text = data["attributes"]["size"]
        pdf.set_font(size=16-((len(text)-5)*2) if len(text) > 5 else 16)
        pdf.cell(text=text, center=True, align="C")

    if "toolsize" in data["attributes"]:
        pdf.set_y(37)
        pdf.set_font(size=8)
        pdf.cell(text=data["attributes"]["toolsize"], center=True, align="C")

    if "type" in data["attributes"]:
        type = data["attributes"]
    elif "category" in data:
        type = data["category"]["name"]
    if len(type) > 0:
        pdf.set_y(41)
        pdf.set_font(size=8)
        pdf.cell(text=type, center=True, align="C")

    if "isodin" in data["attributes"]:
        pdf.set_y(45)
        pdf.set_font(size=8)
        pdf.cell(text=data["attributes"]["isodin"], center=True, align="C")

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


# Location narrowlandscape (Dymo 99010 / S0722370)
def location_narrowlandscape(data):
    labelx = 28
    labely = 89
    pdf = start_label(labelx, labely, orientation='landscape')

    qrsize = 22

    pdf.set_xy(32, 5)
    pdf.set_font(size=30)
    pdf.cell(text=f"**{data['name']}**", markdown=True, align="L")

    pdf.set_xy(32, 17)
    pdf.set_font(size=20)
    pdf.cell(text=data['id'], markdown=True, align="L")

    img = qrcode.make(data["id"], border=0)
    pdf.image(img.get_image(), x=7, y=((labelx-qrsize)/2), w=qrsize)

    printer = get_printer(labelx, labely)
    finish_label(pdf, printer)
